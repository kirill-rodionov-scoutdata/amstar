from uuid import UUID

from app.app_layer.interfaces.services.bookings.get_history_by_id.service import (
    AbstractGetBookingHistoryService,
)
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.app_layer.interfaces.services.bookings.get_history_by_id.dto import BookingStatusHistoryDTO
from app.domain.bookings.exceptions import BookingNotFoundError


class GetBookingHistoryService(AbstractGetBookingHistoryService):
    def __init__(self, uow: AbcUnitOfWork) -> None:
        self.uow = uow

    async def process(self, booking_id: UUID) -> list[BookingStatusHistoryDTO]:
        async with self.uow as uow:
            await uow.booking_repo.get_by_id(booking_id)

            history = await uow.booking_repo.get_status_history(booking_id)
            if not history:
                raise BookingNotFoundError

            return history
