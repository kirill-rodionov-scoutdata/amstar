import uuid
from datetime import UTC, datetime

from app.app_layer.interfaces.services.items.create_item.dto import CreateItemRequest
from app.app_layer.interfaces.services.items.create_item.service import AbstractCreateItemService
from app.app_layer.interfaces.unit_of_work.uow import AbcUnitOfWork
from app.domain.items.dto import ItemDTO
from app.domain.items.entities import ItemEntity


class CreateItemService(AbstractCreateItemService):
    def __init__(self, uow: AbcUnitOfWork) -> None:
        self._uow = uow

    async def process(self, data: CreateItemRequest) -> ItemEntity:
        dto = ItemDTO(
            id=uuid.uuid4(),
            title=data.title,
            description=data.description,
            created_at=datetime.now(UTC),
        )
        entity = ItemEntity(data=dto)

        async with self._uow as uow:
            entity = await uow.item_repo.create(entity)
            await uow.commit()

        return entity
