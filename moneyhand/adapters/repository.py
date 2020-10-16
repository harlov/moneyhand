from contextvars import ContextVar
from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSessionTransaction,
)

from moneyhand.core import entities
from moneyhand.core.repository import AbstractCategoryRepository
from moneyhand.core.repository import AbstractIncomeRepository
from moneyhand.adapters import orm


class BaseAlchemyRepository:
    def __init__(self, uow_context_cv: ContextVar):
        self._context_cv = uow_context_cv

    @property
    def _transaction(self) -> AsyncSessionTransaction:
        return self._context_cv.get().session


class CategoryRepository(BaseAlchemyRepository, AbstractCategoryRepository):
    async def add(self, category: entities.Category) -> None:
        self._transaction.add(self._entity_to_row(category))

    async def list(self) -> List[entities.Category]:
        res = await self._transaction.execute(select(orm.Category))
        return [self._row_to_entity(row) for row in res.scalars()]

    def _row_to_entity(self, row: dict) -> entities.Category:
        return entities.Category(
            id=UUID(row.id),
            name=row.name,
        )

    def _entity_to_row(self, category: entities.Category):
        return orm.Category(
            id=str(category.id),
            name=category.name,
        )


class IncomeRepository(BaseAlchemyRepository, AbstractIncomeRepository):
    async def save(self, income: entities.Income) -> None:
        self._transaction.add(self._entity_to_row(income, 1))
        self._transaction.add(self._entity_to_row(income, 2))

    async def get(self) -> entities.Income:
        res = await self._transaction.execute(select(orm.Income))
        income = entities.Income()

        for row in res.scalars():
            income.set_for(row.seq_num, row.amount)

        return income

    def _entity_to_row(self, income: entities.Income, part):
        part_obj = getattr(income, f"part_{part}")

        return orm.Income(
            id=str(part_obj.id),
            seq_num=part,
            amount=part_obj.amount,
        )


__all__ = ["CategoryRepository", "IncomeRepository"]
