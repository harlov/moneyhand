import pytest
from moneyhand.core import entities


@pytest.fixture
def category_food() -> entities.Category:
    return entities.Category(
        id=entities.new_id(), name="Food", type=entities.CategoryType.NECESSARY
    )


@pytest.fixture
def category_rent() -> entities.Category:
    return entities.Category(
        id=entities.new_id(), name="Rent", type=entities.CategoryType.NECESSARY
    )


@pytest.fixture
def spending_plan(category_food, category_rent) -> entities.SpendingPlan:
    return entities.SpendingPlan(
        id=entities.new_id(),
        is_template=True,
        items=[
            entities.SpendingPlanItem(
                category_id=category_food.id, part_1=100.0, part_2=100.0
            ),
            entities.SpendingPlanItem(
                category_id=category_rent.id, part_1=250.0, part_2=200.0
            ),
        ],
    )


@pytest.fixture
def empty_spending_plan() -> entities.SpendingPlan:
    return entities.SpendingPlan(id=entities.new_id(), is_template=True, items=[])


@pytest.fixture
def income() -> entities.Income:
    return entities.Income(
        id=entities.new_id(),
        is_template=True,
        part_1=400,
        part_2=200,
    )
