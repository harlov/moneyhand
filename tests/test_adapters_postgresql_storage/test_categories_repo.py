import pytest

from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork
from moneyhand.core.entities import Category, new_id, CategoryType

pytestmark = pytest.mark.asyncio


async def test_list(
    unit_of_work_pg: UnitOfWork, pg_category_food: Category, pg_category_rent: Category
):
    async with unit_of_work_pg:
        all_categories = await unit_of_work_pg.category.list()

    assert all_categories == [pg_category_food, pg_category_rent]


async def test_get(unit_of_work_pg: UnitOfWork, pg_category_food: Category):
    async with unit_of_work_pg:
        category = await unit_of_work_pg.category.get(pg_category_food.id)

    assert category == pg_category_food


async def test_get_not_exists(unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        category = await unit_of_work_pg.category.get(new_id())

    assert category is None


@pytest.mark.usefixtures("pg_category_food")
async def test_find(unit_of_work_pg: UnitOfWork, pg_category_rent: Category):
    async with unit_of_work_pg:
        category = await unit_of_work_pg.category.find(name="Rent")

    assert category == pg_category_rent


async def test_create(unit_of_work_pg: UnitOfWork, pg_category_food: Category):
    async with unit_of_work_pg:
        new_cat = Category(
            id=new_id(), name="New test category", type=CategoryType.GOAL
        )

        await unit_of_work_pg.category.save(new_cat)

    async with unit_of_work_pg:
        all_categories = await unit_of_work_pg.category.list()
        assert all_categories == [pg_category_food, new_cat]


async def test_update(unit_of_work_pg: UnitOfWork, pg_category_food: Category):
    pg_category_food.name = "Food Changed Name"

    async with unit_of_work_pg:
        await unit_of_work_pg.category.save(pg_category_food)

    async with unit_of_work_pg:
        all_categories = await unit_of_work_pg.category.list()

    assert all_categories == [pg_category_food]
