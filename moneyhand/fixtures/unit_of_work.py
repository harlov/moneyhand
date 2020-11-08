import contextvars
from copy import deepcopy
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from typing import Type, Dict

import pytest


from moneyhand.core.unit_of_work import AbstractUnitOfWork
from moneyhand.core.repository import AbstractCategoryRepository
from moneyhand.core.repository import AbstractIncomeRepository
from moneyhand.core.repository import AbstractSpendingPlanRepository

from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork


from moneyhand.core import entities


class Store(BaseModel):
    categories: Dict[UUID, entities.Category] = Field(default_factory=dict)
    incomes: entities.Income = Field(default_factory=dict)
    spending_plan: entities.SpendingPlan = Field(default_factory=dict)


@pytest.fixture
def store() -> Store:
    return Store()


@pytest.fixture
def unit_of_work_memory_cls(
    store,
    repository_category_in_memory,
    repository_income_in_memory,
    repository_spending_plan_in_memory,
) -> Type[AbstractUnitOfWork]:
    class UnitOfWorkContext(BaseModel):
        class Config:
            arbitrary_types_allowed = True

        category: AbstractCategoryRepository
        income: AbstractIncomeRepository
        spending_plan: AbstractSpendingPlanRepository
        temp_store: Store

    class InMemoryUnitOfWork(AbstractUnitOfWork):
        def __init__(self):
            self._store = store
            self._context = contextvars.ContextVar("_context")
            super(InMemoryUnitOfWork, self).__init__()

        async def __aenter__(self):
            await super().__aenter__()
            temp_store = deepcopy(self._store)

            c = UnitOfWorkContext(
                category=repository_category_in_memory(temp_store),
                income=repository_income_in_memory(temp_store),
                spending_plan=repository_spending_plan_in_memory(temp_store),
                temp_store=temp_store,
            )
            self._context.set(c)

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            await super().__aexit__(exc_type, exc_val, exc_tb)
            self._context.set(None)

        @property
        def category(self) -> AbstractCategoryRepository:
            c: UnitOfWorkContext = self._context.get()
            return c.category

        @property
        def income(self) -> AbstractIncomeRepository:
            c: UnitOfWorkContext = self._context.get()
            return c.income

        @property
        def spending_plan(self) -> AbstractSpendingPlanRepository:
            c: UnitOfWorkContext = self._context.get()
            return c.spending_plan

        async def commit(self):
            c: UnitOfWorkContext = self._context.get()
            self._store = c.temp_store

        async def rollback(self):
            pass

    return InMemoryUnitOfWork


@pytest.fixture
def unit_of_work_memory(unit_of_work_memory_cls) -> AbstractUnitOfWork:
    return unit_of_work_memory_cls()


@pytest.fixture
def unit_of_work_pg(test_db):
    return UnitOfWork()
