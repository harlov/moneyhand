from typing import List, Type, Optional
from uuid import UUID

import pytest

from moneyhand.core import entities
from moneyhand.core.repository import AbstractCategoryRepository
from moneyhand.core.repository import AbstractIncomeRepository
from moneyhand.core.repository import AbstractSpendingPlanRepository


class BaseInMemoryRepo:
    def __init__(self, init_store):
        self._store = init_store


@pytest.fixture
def repository_category_in_memory() -> Type[AbstractCategoryRepository]:
    class InMemoryCategoryRepository(BaseInMemoryRepo, AbstractCategoryRepository):
        async def save(self, category: entities.Category) -> None:
            self.collection[category.id] = category

        @property
        def collection(self):
            return self._store.categories

        async def get(self, pk: UUID) -> Optional[entities.Category]:
            return self.collection.get(pk)

        async def find(self, name: str) -> Optional[entities.Category]:
            for item in self.collection.values():
                if item.name == name:
                    return item

            return None

        async def list(self) -> List[entities.Category]:
            return list(self.collection.values())

    return InMemoryCategoryRepository


@pytest.fixture
def repository_income_in_memory() -> Type[AbstractIncomeRepository]:
    class InMemoryIncomeRepository(BaseInMemoryRepo, AbstractIncomeRepository):
        @property
        def collection(self):
            return self._store.incomes

        @collection.setter
        def collection(self, income):
            self._store.incomes = income

        async def save(self, income: entities.Income) -> None:
            self.collection[income.id] = income

        async def get(self) -> Optional[entities.Income]:
            try:
                return list(self.collection.values())[0]
            except IndexError:
                return None

    return InMemoryIncomeRepository


@pytest.fixture
def repository_spending_plan_in_memory() -> Type[AbstractSpendingPlanRepository]:
    class InMemorySpendingPlanRepository(
        BaseInMemoryRepo, AbstractSpendingPlanRepository
    ):
        @property
        def collection(self):
            return self._store.spending_plan

        @collection.setter
        def collection(self, spending_plan):
            self._store.spending_plan = spending_plan

        async def save(self, spending_plan: entities.SpendingPlan) -> None:
            self.collection[spending_plan.id] = spending_plan

        async def get(self) -> Optional[entities.SpendingPlan]:
            try:
                return list(self.collection.values())[0]
            except IndexError:
                return None

    return InMemorySpendingPlanRepository
