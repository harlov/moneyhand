import abc
from typing import List, Optional
from uuid import UUID

from . import entities


class AbstractCategoryRepository(abc.ABC):
    @abc.abstractmethod
    async def save(self, category: entities.Category) -> None:
        ...

    @abc.abstractmethod
    async def get(self, pk: UUID) -> Optional[entities.Category]:
        ...

    @abc.abstractmethod
    async def find(self, name: str) -> Optional[entities.Category]:
        ...

    @abc.abstractmethod
    async def list(self) -> List[entities.Category]:
        ...


class AbstractIncomeRepository(abc.ABC):
    @abc.abstractmethod
    async def save(self, income: entities.Income) -> None:
        ...

    @abc.abstractmethod
    async def get(self) -> Optional[entities.Income]:
        ...


class AbstractSpendingPlanRepository(abc.ABC):
    @abc.abstractmethod
    async def save(self, plan: entities.SpendingPlan) -> None:
        ...

    @abc.abstractmethod
    async def get(self) -> Optional[entities.SpendingPlan]:
        ...
