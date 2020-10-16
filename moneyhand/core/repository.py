import abc
from typing import List

from . import entities


class AbstractCategoryRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, category: entities.Category) -> None:
        ...

    @abc.abstractmethod
    async def list(self) -> List[entities.Category]:
        ...


class AbstractIncomeRepository(abc.ABC):
    @abc.abstractmethod
    async def save(self, income: entities.Income) -> None:
        ...

    @abc.abstractmethod
    async def get(self) -> entities.Income:
        ...
