from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.bookings.entities import BookingEntity


class AbstractGetBookingService(ABC):
    @abstractmethod
    async def process(self, booking_id: UUID) -> BookingEntity:
        raise NotImplementedError
