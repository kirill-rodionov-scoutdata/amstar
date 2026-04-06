from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.app_layer.interfaces.repositories.item import AbstractItemRepository
from app.domain.items.dto import ItemDTO
from app.domain.items.entities import ItemEntity
from app.infra.db.models import ItemORM


class ItemRepository(AbstractItemRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, item: ItemEntity) -> ItemEntity:
        orm_obj = ItemORM(
            id=str(item.data.id),
            title=item.data.title,
            description=item.data.description,
        )
        self._session.add(orm_obj)
        await self._session.flush()
        await self._session.refresh(orm_obj)
        return self._to_entity(orm_obj)

    async def get_by_id(self, item_id: UUID) -> ItemEntity | None:
        result = await self._session.execute(select(ItemORM).where(ItemORM.id == str(item_id)))
        orm_obj = result.scalar_one_or_none()
        if orm_obj is None:
            return None
        return self._to_entity(orm_obj)

    def _to_entity(self, orm_obj: ItemORM) -> ItemEntity:
        dto = ItemDTO(
            id=UUID(orm_obj.id),
            title=orm_obj.title,
            description=orm_obj.description,
            created_at=orm_obj.created_at,
        )
        return ItemEntity(data=dto)
