from uuid import UUID

from moneyhand.core import entities
from moneyhand.core import errors
from moneyhand.core.unit_of_work import AbstractUnitOfWork


class SpendingPlanService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def set_for_category(
        self, pk: UUID, category_id: UUID, part: int, amount: float
    ) -> entities.SpendingPlan:
        async with self.uow:
            category = await self.uow.category.get(category_id)
            if category is None:
                raise errors.EntityNotFound("category", category_id)

            spending_plan = await self.uow.spending_plan.get(pk)

            if spending_plan is None:
                spending_plan = entities.SpendingPlan(
                    id=entities.new_id(), is_template=True
                )

            spending_plan.set_for_category(category_id, part, amount)
            await self.uow.spending_plan.save(spending_plan)

            return await self.uow.spending_plan.get(pk)

    async def get(self, pk: UUID):
        async with self.uow:
            return await self.uow.spending_plan.get(pk)

    async def get_active(
        self,
    ) -> entities.SpendingPlan:
        async with self.uow:
            all_ = await self.uow.spending_plan
            return await self.uow.spending_plan.get()
