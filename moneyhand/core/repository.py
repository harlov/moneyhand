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
