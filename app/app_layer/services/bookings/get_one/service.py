from uuid import UUID

from app.app_layer.interfaces.services.bookings.get_one.service import AbstractGetBookingService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.bookings.entities import BookingEntity


class GetBookingService(AbstractGetBookingService):
    def __init__(self, uow: AbcUnitOfWork) -> None:
        self.uow = uow

    async def process(self, booking_id: UUID) -> BookingEntity:
        return await self._fetch(booking_id)

    async def _fetch(self, booking_id: UUID) -> BookingEntity:
        async with self.uow as uow:
            return await uow.booking_repo.get_by_id(booking_id)
