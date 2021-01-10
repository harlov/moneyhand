import pytest

from moneyhand.core import entities
from moneyhand.core.unit_of_work import AbstractUnitOfWork


@pytest.fixture
async def mem_tenant(tenant: entities.Tenant, unit_of_work_memory: AbstractUnitOfWork):
    async with unit_of_work_memory:
        await unit_of_work_memory.tenant.save(tenant)
    return tenant


@pytest.fixture
async def mem_user(user: entities.User, unit_of_work_memory: AbstractUnitOfWork):
    async with unit_of_work_memory:
        await unit_of_work_memory.user.save(user)
    return user


@pytest.fixture
async def mem_category_food(
    category_food: entities.Category, unit_of_work_memory: AbstractUnitOfWork
):
    async with unit_of_work_memory:
        await unit_of_work_memory.category.save(category_food)
    return category_food


@pytest.fixture
async def mem_income(income: entities.Income, unit_of_work_memory: AbstractUnitOfWork):
    async with unit_of_work_memory:
        await unit_of_work_memory.income.save(income)
    return income


@pytest.fixture
async def mem_spending_plan(
    spending_plan: entities.SpendingPlan, unit_of_work_memory: AbstractUnitOfWork
):
    async with unit_of_work_memory:
        await unit_of_work_memory.spending_plan.save(spending_plan)
    return spending_plan
