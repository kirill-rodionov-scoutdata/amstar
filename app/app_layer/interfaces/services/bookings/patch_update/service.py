from abc import ABC, abstractmethod

from app.app_layer.interfaces.services.bookings.patch_update.dto import BatchUpdateStatusInputData
from app.domain.bookings.entities import BookingEntity


class AbstractBatchUpdateStatusService(ABC):
    @abstractmethod
    async def process(self, data: BatchUpdateStatusInputData) -> list[BookingEntity]:
        raise NotImplementedError
