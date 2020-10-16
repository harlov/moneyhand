import abc

from .repository import AbstractCategoryRepository
from .repository import AbstractIncomeRepository


class AbstractUnitOfWork(abc.ABC):
    category: AbstractCategoryRepository
    income: AbstractIncomeRepository

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
        # await self.rollback()
