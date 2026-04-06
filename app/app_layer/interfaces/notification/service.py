from abc import ABC, abstractmethod
from uuid import UUID


class AbstractStatusNotificationService(ABC):
    @abstractmethod
    async def notify_booking_confirmed(self, booking_id: UUID) -> None:
        raise NotImplementedError
