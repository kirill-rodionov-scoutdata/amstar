from abc import ABC, abstractmethod

from app.app_layer.interfaces.services.items.create_item.dto import CreateItemRequest
from app.domain.items.entities import ItemEntity


class AbstractCreateItemService(ABC):
    @abstractmethod
    async def process(self, data: CreateItemRequest) -> ItemEntity:
        raise NotImplementedError
