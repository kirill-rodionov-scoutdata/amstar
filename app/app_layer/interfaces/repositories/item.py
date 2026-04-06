from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.items.entities import ItemEntity


class AbstractItemRepository(ABC):
    @abstractmethod
    async def create(self, item: ItemEntity) -> ItemEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> ItemEntity | None:
        raise NotImplementedError
