import uuid
from datetime import UTC, datetime

from app.app_layer.interfaces.services.bookings.create_booking.dto import CreateBookingRequest
from app.app_layer.interfaces.services.bookings.create_booking.service import AbstractCreateBookingService
from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.entities import BookingEntity
from app.domain.bookings.enums import BookingStatusEnum


class CreateBookingService(AbstractCreateBookingService):
    async def process(self, data: CreateBookingRequest) -> BookingEntity:
        return self._build_entity(data)

    def _build_entity(self, data: CreateBookingRequest) -> BookingEntity:
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
