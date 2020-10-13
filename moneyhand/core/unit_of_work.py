import abc

from .repository import AbstractCategoryRepository


class AbstractUnitOfWork(abc.ABC):
    category: AbstractCategoryRepository

    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
        #await self.rollback()
