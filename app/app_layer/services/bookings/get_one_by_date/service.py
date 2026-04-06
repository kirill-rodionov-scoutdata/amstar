from datetime import date

from app.app_layer.interfaces.services.bookings.get_one_by_date.service import (
    AbstractGetBookingsByDateService,
)
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.bookings.entities import BookingEntity


class GetBookingsByDateService(AbstractGetBookingsByDateService):
    def __init__(self, uow: AbcUnitOfWork) -> None:
        self.uow = uow

    async def process(self, booking_date: date) -> list[BookingEntity]:
        async with self.uow as uow:
            entities = await uow.booking_repo.get_by_date(booking_date)
        return entities
