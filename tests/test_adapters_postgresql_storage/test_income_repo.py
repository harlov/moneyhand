import pytest

from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork
from moneyhand.core.entities import Income, new_id

pytestmark = pytest.mark.asyncio


async def test_get(pg_income: Income, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        income = await unit_of_work_pg.income.get()
    assert income == pg_income


async def test_get_not_exists(unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        income = await unit_of_work_pg.income.get()
    assert income is None


async def test_update_income(unit_of_work_pg: UnitOfWork, pg_income: Income):
    async with unit_of_work_pg:
        pg_income.part_1 = 500
        await unit_of_work_pg.income.save(pg_income)

    async with unit_of_work_pg:
        income = await unit_of_work_pg.income.get()

    assert pg_income == income
