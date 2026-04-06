from datetime import datetime

from sqlalchemy import UUID, insert

from app.app_layer.interfaces.repositories.notification import AbstractNotificationRepository
from app.infra.db.models import NotificationORM
from sqlalchemy.ext.asyncio import AsyncSession


class NotificationRepository(AbstractNotificationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_notification(
        self,
        booking_id: UUID,
        message: str,
        sent_at: datetime,
    ) -> None:
        await self.session.execute(
            insert(NotificationORM).values(
                transfer_id=str(booking_id),
                message=message,
                sent_at=sent_at,
            )
        )
