from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class AbstractNotificationRepository(ABC):
    @abstractmethod
    async def create_notification(
        self,
        booking_id: UUID,
        message: str,
        sent_at: datetime,
    ) -> None:
        raise NotImplementedError
