from abc import ABC, abstractmethod
from uuid import UUID

from app.app_layer.interfaces.services.bookings.get_history_by_id.dto import BookingStatusHistoryDTO


class AbstractGetBookingHistoryService(ABC):
    @abstractmethod
    async def process(self, booking_id: UUID) -> list[BookingStatusHistoryDTO]:
        pass
