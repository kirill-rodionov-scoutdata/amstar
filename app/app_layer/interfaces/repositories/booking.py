from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domain.bookings.entities import BookingEntity
from app.domain.bookings.enums import BookingStatusEnum


class AbstractBookingRepository(ABC):
    @abstractmethod
    async def create(self, booking: BookingEntity) -> BookingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, booking_id: UUID) -> BookingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_ids(self, booking_ids: list[UUID]) -> list[BookingEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, booking_id: UUID, new_status: BookingStatusEnum) -> BookingEntity:
        raise NotImplementedError

    @abstractmethod
    async def create_status_history(
        self,
        booking_id: UUID,
        old_status: BookingStatusEnum,
        new_status: BookingStatusEnum,
        changed_at: datetime,
    ) -> None:
        raise NotImplementedError
