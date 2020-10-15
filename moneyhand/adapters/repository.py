from contextvars import ContextVar
from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncTransaction, AsyncSessionTransaction, \
    AsyncSession

from moneyhand.adapters.unit_of_work_context import UnitOfWorkContext
from moneyhand.core import entities
from moneyhand.core.repository import AbstractCategoryRepository
from moneyhand.adapters import sql_tables
from moneyhand.adapters import orm


class CategoryRepository(AbstractCategoryRepository):
    def __init__(self, uow_context_cv: ContextVar):
        self._context_cv = uow_context_cv

    @property
    def _transaction(self) -> AsyncSessionTransaction:
        return self._context_cv.get().session

    async def add(self, category: entities.Category) -> None:
        self._transaction.add(
            self._entity_to_row(category)
        )

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


__all__ = ["CategoryRepository"]
