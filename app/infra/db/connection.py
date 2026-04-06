import orjson
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import DatabaseSettings
from app.infra.db.utils import orjson_dumper


class AlchemyDatabase:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._engine = create_async_engine(
            str(settings.URL),
            pool_size=settings.POOL_SIZE,
            pool_pre_ping=True,
            json_serializer=orjson_dumper,
            json_deserializer=orjson.loads,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    @property
    def session_factory(self) -> async_sessionmaker:
        return self._session_factory
