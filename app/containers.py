from collections.abc import AsyncIterator

from dependency_injector import containers, providers

from app.app_layer.providers.jwt import JwtProvider
from app.app_layer.services.bookings.create_booking.service import CreateBookingService
from app.config import settings
from app.infra.db.connection import AlchemyDatabase
from app.infra.unit_of_work.uow import Uow


async def get_db_resource(db_settings) -> AsyncIterator[AlchemyDatabase]:
    db = AlchemyDatabase(settings=db_settings)
    yield db
    await db.dispose()


class Container(containers.DeclarativeContainer):
    db = providers.Resource(get_db_resource, db_settings=settings.DB)

    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)

    jwt_provider = providers.Singleton(
        JwtProvider,
        secret=settings.JWT.SECRET,
        algo=settings.JWT.ALGO,
        ttl_seconds=settings.JWT.TTL,
    )


    create_booking_service = providers.Factory(CreateBookingService, uow=uow)
