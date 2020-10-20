from uuid import UUID

from .unit_of_work import AbstractUnitOfWork
from . import entities
from . import errors
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

    async def set_income(self, part: int, amount: float) -> entities.Income:
        async with self.uow:
            income = await self.uow.income.get()
            if income is None:
                income = entities.Income()

            income.set_for(part, amount)

            await self.uow.income.save(income)
            await self.uow.commit()
            return income

    async def get_income(self) -> entities.Income:
        async with self.uow:
            return await self.uow.income.get()

    async def set_spend_for_category(
        self, category_id: UUID, part: int, amount: float
    ) -> entities.SpendingPlan:
        async with self.uow:
            category = await self.uow.category.get(category_id)
            if category is None:
                raise errors.EntityNotFound("category", category_id)

            spending_plan = await self.uow.spending_plan.get()

            if spending_plan is None:
                spending_plan = entities.SpendingPlan()

            spending_plan.set_for_category(category_id, part, amount)
            await self.uow.spending_plan.save(spending_plan)
            await self.uow.commit()

            return await self.uow.spending_plan.get()

    async def get_spending_plan(self) -> entities.SpendingPlan:
        async with self.uow:
            return await self.uow.spending_plan.get()
