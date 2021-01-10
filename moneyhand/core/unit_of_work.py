import abc

from .repository import AbstractUserRepository
from .repository import AbstractTenantRepository
from .repository import AbstractCategoryRepository
from .repository import AbstractIncomeRepository
from .repository import AbstractSpendingPlanRepository


class AbstractUnitOfWork(abc.ABC):
    user: AbstractUserRepository
    tenant: AbstractTenantRepository
    category: AbstractCategoryRepository
    income: AbstractIncomeRepository
    spending_plan: AbstractSpendingPlanRepository

    autocommit: bool

    def __init__(self, autocommit: bool = True) -> None:
        self.autocommit = autocommit

    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...

    @abc.abstractmethod
    async def setup(self):
        ...

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.autocommit:
            await self.commit()
        else:
            await self.rollback()
