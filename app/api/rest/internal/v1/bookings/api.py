from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.app_layer.interfaces.services.bookings.create_booking.dto import CreateBookingRequest
from app.app_layer.interfaces.services.bookings.create_booking.exceptions import (
    BookingFlightNotFoundError,
    BookingUnauthorizedError,
    BookingValidationError,
)
from app.app_layer.interfaces.services.bookings.create_booking.service import AbstractCreateBookingService
from app.app_layer.interfaces.services.bookings.get_booking.service import AbstractGetBookingService
from app.containers import Container
from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.exceptions import BookingNotFoundError

router = APIRouter()


@router.post("", response_model=BookingDTO, status_code=status.HTTP_201_CREATED)
@inject
async def create_booking(
    data: CreateBookingRequest,
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
