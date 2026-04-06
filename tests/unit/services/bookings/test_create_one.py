import pytest
from app.app_layer.services.bookings.create_one.service import CreateBookingService
from app.app_layer.interfaces.services.bookings.create_one.dto import CreateBookingInputData
from app.domain.bookings.entities import BookingEntity
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_create_booking_success(mock_uow, mock_booking_repo, booking_entity_factory, load_json_data):
    # Arrange
    service = CreateBookingService(uow=mock_uow)
    test_cases = load_json_data("create_booking_valid.json")
    
    for case in test_cases:
        data = CreateBookingInputData(**case)
        expected_entity = booking_entity_factory(passenger_name=data.passenger_name)
        mock_booking_repo.create.return_value = expected_entity
        
        # Act
        result = await service.process(data)
        
        # Assert
        assert isinstance(result, BookingEntity)
        assert result.data.passenger_name == data.passenger_name
        mock_booking_repo.create.assert_called()
        mock_booking_repo.create.reset_mock()
