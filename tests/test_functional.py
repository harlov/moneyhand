import pytest

from moneyhand.app import create_service

pytestmark = pytest.mark.skip()


@pytest.fixture
async def service():
    return await create_service()


@pytest.mark.asyncio
async def test_add_and_view_categories(service):
    food_category = await service.create_category("Food")
    all_categories = await service.get_categories()
    assert all_categories == [food_category]

    rent_category = await service.create_category("Rent")
    all_categories = await service.get_categories()
    assert all_categories == [food_category, rent_category]
