from datetime import date
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from app.app_layer.interfaces.services.bookings.get_one_by_date.service import AbstractGetBookingsByDateService
from app.app_layer.interfaces.services.bookings.patch_update.dto import BatchUpdateStatusInputData
from app.app_layer.interfaces.services.bookings.patch_update.exceptions import (
    BatchBookingNotFoundError,
    BatchInvalidTransitionError,
)
from app.app_layer.interfaces.services.bookings.patch_update.service import AbstractBatchUpdateStatusService
from app.app_layer.interfaces.services.bookings.create_one.dto import CreateBookingInputData
from app.app_layer.interfaces.services.bookings.create_one.exceptions import (
    BookingFlightNotFoundError,
    BookingUnauthorizedError,
    BookingValidationError,
)
from app.app_layer.interfaces.services.bookings.create_one.service import AbstractCreateBookingService
from app.app_layer.interfaces.services.bookings.get_one.service import AbstractGetBookingService
from app.containers import Container
from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.enums import BookingStatusEnum
from app.domain.bookings.exceptions import BookingNotFoundError

router = APIRouter()


@router.post("", response_model=BookingDTO, status_code=status.HTTP_201_CREATED)
@inject
async def create_booking(
    data: CreateBookingInputData,
    service: AbstractCreateBookingService = Depends(Provide[Container.create_booking_service]),
) -> BookingDTO:
    try:
        entity = await service.process(data)
    except BookingValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except BookingUnauthorizedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except BookingFlightNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return entity.data


@router.patch("/batch-status", response_model=list[BookingDTO], status_code=status.HTTP_200_OK)
@inject
async def batch_update_booking_status(
    data: BatchUpdateStatusInputData,
    background_tasks: BackgroundTasks,
    service: AbstractBatchUpdateStatusService = Depends(Provide[Container.batch_update_status_service]),
) -> list[BookingDTO]:
    try:
        entities = await service.process(data)
    except BatchBookingNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "bookings_not_found", "missing_ids": exc.missing_ids},
        )
    except BatchInvalidTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "invalid_transition",
                "booking_id": exc.booking_id,
                "from_status": exc.from_status,
                "to_status": exc.to_status,
            },
        )
    for entity in entities:
        if entity.data.status == BookingStatusEnum.CONFIRMED:
            background_tasks.add_task(_send_confirmation_notification, str(entity.data.id))
    return [entity.data for entity in entities]


async def _send_confirmation_notification(booking_id: str) -> None:
    # Placeholder for outbound delivery (email, SMS, push).
    # Runs after response is sent; failures here do not affect the HTTP response.
    pass


@router.get("/{booking_id}", response_model=BookingDTO, status_code=status.HTTP_200_OK)
@inject
async def get_booking(
    booking_id: UUID,
    service: AbstractGetBookingService = Depends(Provide[Container.get_booking_service]),
) -> BookingDTO:
    try:
        entity = await service.process(booking_id)
    except BookingNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return entity.data


@router.get("", response_model=list[BookingDTO], status_code=status.HTTP_200_OK)
@inject
async def get_bookings_by_date(
    pickup_date: date,
    service: AbstractGetBookingsByDateService = Depends(
        Provide[Container.get_bookings_by_date_service]
    ),
) -> list[BookingDTO]:
    entities = await service.process(pickup_date)
    return [entity.data for entity in entities]
