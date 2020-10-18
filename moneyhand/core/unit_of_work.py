import abc

from .repository import AbstractCategoryRepository
from .repository import AbstractIncomeRepository
from .repository import AbstractSpendingPlanRepository


class AbstractUnitOfWork(abc.ABC):
    category: AbstractCategoryRepository
    income: AbstractIncomeRepository
    spending_plan: AbstractSpendingPlanRepository

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
