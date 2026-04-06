from collections.abc import AsyncIterator

from dependency_injector import containers, providers

from app.app_layer.providers.jwt import JwtProvider
from app.app_layer.services.bookings.get_one_by_date.service import GetBookingsByDateService
from app.app_layer.services.bookings.patch_update.service import BatchUpdateStatusService
from app.app_layer.services.bookings.create_one.service import CreateBookingService
from app.app_layer.services.bookings.get_one.service import GetBookingService
from app.app_layer.services.bookings.get_history_by_id.service import GetBookingHistoryService
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

    get_booking_service = providers.Factory(GetBookingService, uow=uow)

    batch_update_status_service = providers.Factory(BatchUpdateStatusService, uow=uow)

    get_bookings_by_date_service = providers.Factory(
        GetBookingsByDateService,
        uow=uow,
    )

    get_booking_history_service = providers.Factory(
    GetBookingHistoryService,
    uow=uow,
    )
