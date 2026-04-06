from datetime import datetime, timezone
import logging
from uuid import UUID

from app.app_layer.interfaces.notification.service import AbstractStatusNotificationService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork

logger = logging.getLogger(__name__)


class NotificationService(AbstractStatusNotificationService):
    def __init__(self, uow: AbcUnitOfWork) -> None:
        self.uow = uow

    async def notify_booking_confirmed(self, booking_id: UUID) -> None:
        message: str = self._build_message(booking_id=booking_id)
        logger.info("Notification task started", extra={"booking_id": str(booking_id)})

        async with self.uow as uow:
            await uow.notification_repo.create_notification(
                booking_id=booking_id,
                message=message,
                sent_at=datetime.now(timezone.utc),
            )

    def _build_message(self, booking_id: UUID) -> str:
        return f"===== Booking {booking_id} has been confirmed ====="
