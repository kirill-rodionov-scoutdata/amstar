from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.app_layer.interfaces.repositories.booking import AbstractBookingRepository
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.infra.repositories.booking.alchemy import BookingRepository


class Uow(AbcUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._booking_repo: BookingRepository | None = None

    async def __aenter__(self) -> "Uow":
        self._session = self._session_factory()
        self._booking_repo = BookingRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.shutdown()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def shutdown(self) -> None:
        await self._session.close()

    @property
    def booking_repo(self) -> AbstractBookingRepository:
        return self._booking_repo
