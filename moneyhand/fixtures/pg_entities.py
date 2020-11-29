import pytest

from moneyhand.core.entities import Income, SpendingPlan, Tenant, User
from moneyhand.core.entities.categories import Category
from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork


@pytest.fixture
async def pg_income(income: Income, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        await unit_of_work_pg.income.save(income)
        return income


@pytest.fixture
async def pg_category_food(category_food: Category, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        await unit_of_work_pg.category.save(category_food)
        return category_food


@pytest.fixture
async def pg_category_rent(category_rent: Category, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        await unit_of_work_pg.category.save(category_rent)
        return category_rent


@pytest.fixture
async def pg_spending_plan(
    spending_plan: SpendingPlan,
    unit_of_work_pg: UnitOfWork,
    pg_category_food,
    pg_category_rent,
):
    async with unit_of_work_pg:
        await unit_of_work_pg.spending_plan.save(spending_plan)

    return spending_plan


@pytest.fixture
async def pg_empty_spending_plan(
    empty_spending_plan: SpendingPlan, unit_of_work_pg: UnitOfWork
):
    async with unit_of_work_pg:
        await unit_of_work_pg.spending_plan.save(empty_spending_plan)

    return empty_spending_plan


@pytest.fixture
async def pg_tenant(tenant: Tenant, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        await unit_of_work_pg.tenant.save(tenant)

    return tenant


@pytest.fixture
async def pg_user(user: User, unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        await unit_of_work_pg.user.save(user)
