from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.bookings.entities import BookingEntity


class AbstractBookingRepository(ABC):
    @abstractmethod
    async def create(self, booking: BookingEntity) -> BookingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, booking_id: UUID) -> BookingEntity:
        raise NotImplementedError
