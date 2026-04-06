from abc import ABC, abstractmethod
from datetime import date

from app.domain.bookings.entities import BookingEntity


class AbstractGetBookingsByDateService(ABC):
    @abstractmethod
    async def process(self, booking_date: date) -> list[BookingEntity]:
        raise NotImplementedError
