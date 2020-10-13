import pytest
from moneyhand.core import entities


@pytest.fixture
def category_food() -> entities.Category:
    return entities.Category(
        id=entities.new_id(),
        name="Food"
    )


@pytest.fixture
def category_rent() -> entities.Category:
    return entities.Category(
        id=entities.new_id(),
        name="Rent"
    )
