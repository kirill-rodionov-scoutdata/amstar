from datetime import datetime
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.app_layer.interfaces.repositories.booking import AbstractBookingRepository
from app.domain.bookings.dto import BookingDTO
from app.domain.bookings.entities import BookingEntity
from app.domain.bookings.enums import BookingStatusEnum
from app.domain.bookings.exceptions import BookingNotFoundError
from app.infra.db.models import BookingORM, BookingStatusHistoryORM, NotificationORM


class BookingRepository(AbstractBookingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, booking: BookingEntity) -> BookingEntity:
        await self._session.execute(
            insert(BookingORM).values(
                id=str(booking.data.id),
                passenger_name=booking.data.passenger_name,
                flight_number=booking.data.flight_number,
                pickup_time=booking.data.pickup_time,
                pickup_location=booking.data.pickup_location,
                dropoff_location=booking.data.dropoff_location,
                status=booking.data.status.value,
            )
        )
        result = await self._session.execute(
            select(BookingORM).where(BookingORM.id == str(booking.data.id))
        )
        return self.to_entity(result.scalar_one())

    async def get_by_id(self, booking_id: UUID) -> BookingEntity:
        result = await self._session.execute(
            select(BookingORM).where(BookingORM.id == str(booking_id))
        )
        orm_obj = result.scalar_one_or_none()
        if orm_obj is None:
            raise BookingNotFoundError(f"Booking '{booking_id}' not found")
        return self.to_entity(orm_obj)

    async def get_by_ids(self, booking_ids: list[UUID]) -> list[BookingEntity]:
        str_ids = [str(bid) for bid in booking_ids]
        result = await self._session.execute(
            select(BookingORM).where(BookingORM.id.in_(str_ids))
        )
        orm_objs = result.scalars().all()
        id_to_entity = {UUID(o.id): self.to_entity(o) for o in orm_objs}
        # Preserve input order; omit IDs not found (caller handles missing check)
        return [id_to_entity[bid] for bid in booking_ids if bid in id_to_entity]

    async def update_status(self, booking_id: UUID, new_status: BookingStatusEnum) -> BookingEntity:
        await self._session.execute(
            update(BookingORM)
            .where(BookingORM.id == str(booking_id))
            .values(status=new_status.value)
        )
        result = await self._session.execute(
            select(BookingORM).where(BookingORM.id == str(booking_id))
        )
        return self.to_entity(result.scalar_one())

    async def create_status_history(
        self,
        booking_id: UUID,
        old_status: BookingStatusEnum,
        new_status: BookingStatusEnum,
        changed_at: datetime,
    ) -> None:
        await self._session.execute(
            insert(BookingStatusHistoryORM).values(
                booking_id=str(booking_id),
                old_status=old_status.value,
                new_status=new_status.value,
                changed_at=changed_at,
            )
        )

    async def create_notification(
        self,
        booking_id: UUID,
        message: str,
        sent_at: datetime,
    ) -> None:
        await self._session.execute(
            insert(NotificationORM).values(
                transfer_id=str(booking_id),
                message=message,
                sent_at=sent_at,
            )
        )

    def to_entity(self, orm_obj: BookingORM) -> BookingEntity:
        dto = BookingDTO(
            id=UUID(orm_obj.id),
            passenger_name=orm_obj.passenger_name,
            flight_number=orm_obj.flight_number,
            pickup_time=orm_obj.pickup_time,
            pickup_location=orm_obj.pickup_location,
            dropoff_location=orm_obj.dropoff_location,
            status=orm_obj.status,
            created_at=orm_obj.created_at,
        )
        return BookingEntity(data=dto)
