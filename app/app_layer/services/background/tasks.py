from uuid import UUID

from app.app_layer.interfaces.notification.service import AbstractStatusNotificationService


async def notify_booking_confirmed_task(
    notification_service: AbstractStatusNotificationService,
    booking_id: UUID,
) -> None:
    await notification_service.notify_booking_confirmed(booking_id=booking_id)
