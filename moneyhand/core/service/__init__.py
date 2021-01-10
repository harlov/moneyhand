from uuid import UUID


from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.core import entities
from moneyhand.core import errors
from typing import List, Optional

from .tenant import TenantService
from .spending_plan import SpendingPlanService


class Service:
    tenant: TenantService
    spending_plan: SpendingPlanService

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow
        self.tenant = TenantService(uow=uow)
        self.spending_plan = SpendingPlanService(uow=uow)

    async def on_startup(self):
        await self.uow.setup()
        await self.tenant.ensure_default()

    async def create_category(
        self, name: str, type_: entities.CategoryType
    ) -> entities.Category:
        async with self.uow:
            category = entities.Category(id=entities.new_id(), name=name, type=type_)
            await self.uow.category.save(category)
            return category

    async def update_category(
        self,
        pk: UUID,
        name: Optional[str] = None,
        type_: Optional[entities.CategoryType] = None,
    ) -> entities.Category:
        async with self.uow:
            category = await self.uow.category.get(pk)

            if category is None:
                raise errors.EntityNotFound("category", pk)

            if name is not None:
                category.name = name
            if type_ is not None:
                category.type = type_

            await self.uow.category.save(category)
            return category

    async def get_categories(self) -> List[entities.Category]:
        async with self.uow:
            return await self.uow.category.list()

    async def find_category(self, name: str) -> Optional[entities.Category]:
        async with self.uow:
            return await self.uow.category.find(name)

    async def set_income(
        self, part_1: Optional[float] = None, part_2: Optional[float] = None
    ) -> entities.Income:
        async with self.uow:
            income = await self.uow.income.get()
            if income is None:
                income = entities.Income(id=entities.new_id(), is_template=True)

            if part_1 is not None:
                income.set_for(1, part_1)

            if part_2 is not None:
                income.set_for(2, part_2)

            await self.uow.income.save(income)
            return income

    async def get_income(self) -> entities.Income:
        async with self.uow:
            return await self.uow.income.get()

    async def get_balance_report(self) -> entities.BalanceReport:
        async with self.uow:
            income = await self.uow.income.get()
            spending_plan = await self.uow.spending_plan.get()
            return entities.BalanceReport.create(
                income=income, spending_plan=spending_plan
            )
