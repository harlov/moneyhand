from .unit_of_work import AbstractUnitOfWork
from . import entities

from typing import List


class Service:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create_category(self, name: str) -> entities.Category:
        async with self.uow:
            category = entities.Category(id=entities.new_id(), name=name)
            await self.uow.category.add(category)
            await self.uow.commit()
            return category

    async def get_categories(self) -> List[entities.Category]:
        async with self.uow:
            return await self.uow.category.list()
