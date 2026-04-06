from abc import ABC, abstractmethod

from app.app_layer.interfaces.services.bookings.create_booking.dto import CreateBookingRequest
from app.domain.bookings.entities import BookingEntity


class AbstractCreateBookingService(ABC):
    @abstractmethod
    async def process(self, data: CreateBookingRequest) -> BookingEntity:
        raise NotImplementedError
