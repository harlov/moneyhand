import pytest
from pydantic import ValidationError

from moneyhand.core import entities
from moneyhand.core.service import Service
from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.core import errors

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def memory_category_food(
    category_food: entities.Category, unit_of_work_memory: AbstractUnitOfWork
):
    async with unit_of_work_memory:
        await unit_of_work_memory.category.save(category_food)
        return category_food


@pytest.fixture
async def memory_category_rent(
    category_rent: entities.Category, unit_of_work_memory: AbstractUnitOfWork
):
    async with unit_of_work_memory:
        await unit_of_work_memory.category.save(category_rent)
        return category_rent


@pytest.fixture
async def memory_income(
    income: entities.Income, unit_of_work_memory: AbstractUnitOfWork
):
    async with unit_of_work_memory:
        await unit_of_work_memory.income.save(income)
        return income


@pytest.fixture
async def memory_spending_plan(
    spending_plan: entities.SpendingPlan,
    unit_of_work_memory: AbstractUnitOfWork,
    memory_category_food,
    memory_category_rent,
):
    async with unit_of_work_memory:
        await unit_of_work_memory.spending_plan.save(spending_plan)
        return spending_plan


async def test_get_categories(
    service_in_memory: Service,
    memory_category_food: entities.Category,
    memory_category_rent: entities.Category,
):
    assert await service_in_memory.get_categories() == [
        memory_category_food,
        memory_category_rent,
    ]


@pytest.mark.usefixtures("memory_category_food")
async def test_find_category(
    service_in_memory: Service, memory_category_rent: entities.Category
):
    category = await service_in_memory.find_category("Rent")
    assert category == memory_category_rent


async def test_create_category(service_in_memory: Service):
    res = await service_in_memory.create_category(
        "Test category", entities.CategoryType.NECESSARY
    )
    assert res.name == "Test category"
    res_get = await service_in_memory.get_categories()
    assert res_get == [res]


async def test_create_invalid_category(service_in_memory: Service):
    with pytest.raises(ValidationError):
        await service_in_memory.create_category("", entities.CategoryType.NECESSARY)

    res_get = await service_in_memory.get_categories()
    assert res_get == []


async def test_update_category(service_in_memory: Service, memory_category_food):
    await service_in_memory.update_category(
        memory_category_food.id, "Food changed name"
    )
    memory_category_food.name = "Food changed name"
    assert await service_in_memory.get_categories() == [memory_category_food]


async def test_set_income_at_first_time(service_in_memory: Service):
    res: entities.Income = await service_in_memory.set_income(part_1=100000)
    assert res.part_1 == 100000
    assert res.part_2 == 0

    res_get = await service_in_memory.get_income()
    assert res_get == res


@pytest.mark.usefixtures("memory_income")
async def test_set_income_if_already_exists(service_in_memory: Service):
    res: entities.Income = await service_in_memory.set_income(part_1=100000)
    assert res.part_1 == 100000
    assert res.part_2 == 200

    res_get = await service_in_memory.get_income()
    assert res_get == res


async def test_get_income(service_in_memory: Service, memory_income: entities.Income):
    income = await service_in_memory.get_income()
    assert income == memory_income


async def test_set_spend_for_category_at_first_time(
    service_in_memory: Service,
    unit_of_work_memory: AbstractUnitOfWork,
    category_food: entities.Category,
    category_rent: entities.Category,
):
    async with unit_of_work_memory:
        await unit_of_work_memory.category.save(category_food)
        await unit_of_work_memory.category.save(category_rent)

    res = await service_in_memory.set_spend_for_category(category_food.id, 1, 10000.0)

    assert res.items == [
        entities.SpendingPlanItem(
            category_id=category_food.id, part_1=10000.0, part_2=0.0
        )
    ]


@pytest.mark.usefixtures("memory_spending_plan")
async def test_set_spend_for_category_if_already_exists(
    service_in_memory: Service,
    category_food: entities.Category,
):
    res = await service_in_memory.set_spend_for_category(category_food.id, 1, 10000.0)

    assert len(res.items) == 2
    assert res.items[0] == entities.SpendingPlanItem(
        category_id=category_food.id, part_1=10000.0, part_2=100.0
    )


async def test_set_spend_for_fake_category(
    service_in_memory: Service,
):

    with pytest.raises(errors.EntityNotFound):
        await service_in_memory.set_spend_for_category(entities.new_id(), 1, 10000.0)


async def test_get_spending_plan(
    service_in_memory: Service, memory_spending_plan: entities.SpendingPlan
):
    plan = await service_in_memory.get_spending_plan()
    assert plan == memory_spending_plan


@pytest.mark.usefixtures("memory_income", "memory_spending_plan")
async def test_get_balance_report(service_in_memory: Service):
    balance = await service_in_memory.get_balance_report()
    assert balance == entities.BalanceReport(
        part_1=50.0,
        part_2=-100.0,
    )
