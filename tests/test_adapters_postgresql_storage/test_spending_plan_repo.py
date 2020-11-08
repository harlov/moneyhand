import pytest

from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork
from moneyhand.core.entities import SpendingPlan

pytestmark = pytest.mark.asyncio


async def test_get(pg_spending_plan: SpendingPlan, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        spending_plan = await unit_of_work_pg.spending_plan.get()

    assert spending_plan == pg_spending_plan


async def test_get_not_exists(unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        spending_plan = await unit_of_work_pg.spending_plan.get()

    assert spending_plan is None


async def test_get_empty(
    pg_empty_spending_plan: SpendingPlan, unit_of_work_pg: UnitOfWork
):
    async with unit_of_work_pg:
        spending_plan = await unit_of_work_pg.spending_plan.get()

    assert spending_plan == pg_empty_spending_plan


async def test_update(pg_spending_plan: SpendingPlan, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        pg_spending_plan.items[0].part_2 = 999
        await unit_of_work_pg.spending_plan.save(pg_spending_plan)

    async with unit_of_work_pg:
        spending_plan = await unit_of_work_pg.spending_plan.get()

    assert spending_plan == pg_spending_plan
