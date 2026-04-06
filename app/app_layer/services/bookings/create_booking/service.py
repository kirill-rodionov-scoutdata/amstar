import uuid
from datetime import UTC, datetime

from app.app_layer.interfaces.services.bookings.create_booking.dto import CreateBookingInputData
from app.app_layer.interfaces.services.bookings.create_booking.service import AbstractCreateBookingService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.entities import BookingEntity
from app.domain.bookings.enums import BookingStatusEnum


class CreateBookingService(AbstractCreateBookingService):
    def __init__(self, uow: AbcUnitOfWork) -> None:
        self.uow = uow

    async def process(self, data: CreateBookingInputData) -> BookingEntity:
        entity = self.build_entity(data)
        async with self.uow as uow:
            entity = await uow.booking_repo.create(entity)
        return entity

    def build_entity(self, data: CreateBookingInputData) -> BookingEntity:
        dto = BookingDTO(
            id=uuid.uuid4(),
            passenger_name=data.passenger_name,
            flight_number=data.flight_number,
            pickup_time=data.pickup_time,
            pickup_location=data.pickup_location,
            dropoff_location=data.dropoff_location,
            status=BookingStatusEnum.PENDING,
            created_at=datetime.now(UTC),
        )
        return BookingEntity(data=dto)
