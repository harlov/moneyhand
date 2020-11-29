from uuid import UUID


from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.core import entities
from moneyhand.core import errors
from typing import List, Optional

from .tenant import TenantService


class Service:
    tenant: TenantService

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
        self.tenant = TenantService(uow=uow)

    async def create_category(
        self, name: str, type_: entities.CategoryType
    ) -> entities.Category:
        async with self.uow:
            category = entities.Category(id=entities.new_id(), name=name, type=type_)
            await self.uow.category.save(category)
            return category

    async def update_category(self, pk: UUID, name: str) -> entities.Category:
        async with self.uow:
            category = await self.uow.category.get(pk)
            category.name = name
            await self.uow.category.save(category)
            return category

    async def get_categories(self) -> List[entities.Category]:
        async with self.uow:
            return await self.uow.category.list()

    async def find_category(self, name: str) -> Optional[entities.Category]:
        async with self.uow:
            return await self.uow.category.find(name)

    async def set_income(self, part: int, amount: float) -> entities.Income:
        async with self.uow:
            income = await self.uow.income.get()
            if income is None:
                income = entities.Income(id=entities.new_id(), is_template=True)

            income.set_for(part, amount)

            await self.uow.income.save(income)
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
                spending_plan = entities.SpendingPlan(
                    id=entities.new_id(), is_template=True
                )

            spending_plan.set_for_category(category_id, part, amount)
            await self.uow.spending_plan.save(spending_plan)

            return await self.uow.spending_plan.get()

    async def get_spending_plan(
        self,
    ) -> entities.SpendingPlan:
        async with self.uow:
            return await self.uow.spending_plan.get()

    async def get_balance_report(self) -> entities.BalanceReport:
        async with self.uow:
            income = await self.uow.income.get()
            spending_plan = await self.uow.spending_plan.get()
            return entities.BalanceReport.create(
                income=income, spending_plan=spending_plan
            )
