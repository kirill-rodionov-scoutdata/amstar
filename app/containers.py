from dependency_injector import containers, providers

from app.app_layer.providers.jwt import JwtProvider
from app.app_layer.services.items.create_item.service import CreateItemService
from app.config import settings
from app.infra.db.connection import AlchemyDatabase
from app.infra.unit_of_work.uow import Uow


class Container(containers.DeclarativeContainer):
    db = providers.Singleton(AlchemyDatabase, settings=settings.DB)

    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)

    jwt_provider = providers.Singleton(
        JwtProvider,
        secret=settings.JWT.SECRET,
        algo=settings.JWT.ALGO,
        ttl_seconds=settings.JWT.TTL,
    )

    create_item_service = providers.Factory(CreateItemService, uow=uow)
