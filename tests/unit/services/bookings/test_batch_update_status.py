import uuid

import pytest

from app.app_layer.interfaces.services.bookings.patch_update.dto import BatchUpdateStatusInputData
from app.app_layer.interfaces.services.bookings.patch_update.exceptions import (
    BatchBookingNotFoundError,
    BatchInvalidTransitionError,
)
from app.app_layer.services.bookings.patch_update.service import BatchUpdateStatusService
from app.domain.bookings.enums import BookingStatusEnum


@pytest.mark.asyncio
async def test_batch_update_status_next_success(mock_uow, mock_booking_repo, booking_entity_factory, load_json_data):
    # Arrange
    service = BatchUpdateStatusService(uow=mock_uow)
    booking_id = uuid.uuid4()
    entity = booking_entity_factory(status=BookingStatusEnum.PENDING)
    entity.data.id = booking_id
    
    mock_booking_repo.get_by_ids.return_value = [entity]
    mock_booking_repo.update_status.return_value = entity
    
    payloads = load_json_data("batch_update_payloads.json")
    data = BatchUpdateStatusInputData(booking_ids=[booking_id], **payloads["action_next"])
    
    # Act
    result = await service.process(data)
    
    # Assert
    assert len(result) == 1
    assert result[0].data.status == BookingStatusEnum.CONFIRMED
    mock_booking_repo.get_by_ids.assert_called_once_with([booking_id])
    mock_booking_repo.update_status.assert_called_once()
    mock_booking_repo.create_status_history.assert_called_once()


@pytest.mark.asyncio
async def test_batch_update_status_not_found_raises(mock_uow, mock_booking_repo):
    # Arrange
    service = BatchUpdateStatusService(uow=mock_uow)
    booking_id = uuid.uuid4()
    mock_booking_repo.get_by_ids.return_value = []
    
    data = BatchUpdateStatusInputData(booking_ids=[booking_id], action="next")
    
    # Act & Assert
    with pytest.raises(BatchBookingNotFoundError):
        await service.process(data)


@pytest.mark.asyncio
async def test_batch_update_status_invalid_transition_raises(mock_uow, mock_booking_repo, booking_entity_factory):
    # Arrange
    service = BatchUpdateStatusService(uow=mock_uow)
    booking_id = uuid.uuid4()
    # Completed status cannot go "next"
    entity = booking_entity_factory(status=BookingStatusEnum.COMPLETED)
    entity.data.id = booking_id
    
    mock_booking_repo.get_by_ids.return_value = [entity]
    
    data = BatchUpdateStatusInputData(booking_ids=[booking_id], action="next")
    
    # Act & Assert
    with pytest.raises(BatchInvalidTransitionError):
        await service.process(data)
