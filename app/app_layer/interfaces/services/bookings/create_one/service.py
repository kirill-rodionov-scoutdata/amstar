from abc import ABC, abstractmethod

from app.app_layer.interfaces.services.bookings.create_one.dto import CreateBookingInputData
from app.domain.bookings.entities import BookingEntity


class AbstractCreateBookingService(ABC):
    @abstractmethod
    async def process(self, data: CreateBookingInputData) -> BookingEntity:
        raise NotImplementedError
