from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.app_layer.interfaces.repositories.item import AbstractItemRepository


class AbcUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> "AbcUnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def item_repo(self) -> "AbstractItemRepository":
        raise NotImplementedError
