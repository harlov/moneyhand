import pytest
from pydantic import ValidationError
from moneyhand.core import entities
from moneyhand.core.service import Service
from moneyhand.core.unit_of_work import AbstractUnitOfWork

pytestmark = pytest.mark.asyncio


async def test_create_category(service_in_memory: Service):
    res = await service_in_memory.create_category("Test category")
    assert res.name == "Test category"
    res_get = await service_in_memory.get_categories()
    assert res_get == [res]


async def test_create_invalid_category(service_in_memory: Service):
    with pytest.raises(ValidationError):
        await service_in_memory.create_category("")

    res_get = await service_in_memory.get_categories()
    assert res_get == []


async def test_set_income(service_in_memory: Service):
    res: entities.Income = await service_in_memory.set_income(1, 100000)
    assert res.part_1.amount == 100000
    assert res.part_2.amount == 0

    res_get = await service_in_memory.get_income()
    assert res_get == res


async def test_set_spend_for_category(
        service_in_memory: Service,
        unit_of_work: AbstractUnitOfWork,
        category_food: entities.Category,
        category_rent: entities.Category,
    ):
    async with unit_of_work:
        await unit_of_work.category.add(category_food)
        await unit_of_work.category.add(category_rent)
        await unit_of_work.commit()

    res = await service_in_memory.set_spend_for_category(category_food.id,
                                                               10000.0)

    assert res.items == [
        entities.SpendingPlanItem(
            category_id=category_food.id,
            amount=10000.0,
        )
    ]
