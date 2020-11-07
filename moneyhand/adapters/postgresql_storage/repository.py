from contextvars import ContextVar
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import (
    AsyncSessionTransaction,
)

from moneyhand.core import entities
from moneyhand.core.repository import AbstractCategoryRepository
from moneyhand.core.repository import AbstractIncomeRepository
from moneyhand.core.repository import AbstractSpendingPlanRepository
from moneyhand.adapters.postgresql_storage import orm


class BaseAlchemyRepository:
    def __init__(self, uow_context_cv: ContextVar):
        self._context_cv = uow_context_cv

    @property
    def _transaction(self) -> AsyncSessionTransaction:
        return self._context_cv.get().session


class CategoryRepository(BaseAlchemyRepository, AbstractCategoryRepository):
    async def get(self, pk: UUID) -> Optional[entities.Category]:
        res = await self._transaction.execute(
            select(orm.Category).filter(orm.Category.id == str(pk)).limit(1)
        )
        return self._row_to_entity(res.scalar())

    async def find(self, name: str) -> Optional[entities.Category]:
        res = await self._transaction.execute(
            select(orm.Category).filter(orm.Category.name == name)
        )
        return self._row_to_entity(res.scalar())

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

    def _entity_to_row(self, income: entities.Income, part) -> orm.Income:
        part_obj = getattr(income, f"part_{part}")

        return orm.Income(
            id=str(uuid4()),
            seq_num=part,
            amount=part_obj.amount,
        )


class SpendingPlanRepository(BaseAlchemyRepository, AbstractSpendingPlanRepository):
    async def save(self, plan: entities.SpendingPlan) -> None:
        await self._transaction.execute(delete(orm.SpendingPlanItem))
        for item in plan.items:
            self._transaction.add(self._item_to_row(item, 1))
            self._transaction.add(self._item_to_row(item, 2))

    async def get(self) -> entities.SpendingPlan:
        res = await self._transaction.execute(select(orm.SpendingPlanItem))
        return self._row_to_entity(res.scalars())

    def _item_to_row(
        self, item: entities.SpendingPlanItem, part: int
    ) -> orm.SpendingPlanItem:
        return orm.SpendingPlanItem(
            id=str(uuid4()),
            category_id=str(item.category_id),
            amount=getattr(item, f"part_{part}"),
            seq_num=part,
        )

    def _row_to_entity(
        self, item_rows: List[orm.SpendingPlanItem]
    ) -> entities.SpendingPlan:
        entity_items = {}

        for item in item_rows:
            entity_item: entities.SpendingPlanItem
            try:
                entity_item = entity_items[item.category_id]
            except KeyError:
                entity_items[
                    item.category_id
                ] = entity_item = entities.SpendingPlanItem(
                    category_id=item.category_id
                )

            entity_item.set_for(item.seq_num, item.amount)

        return entities.SpendingPlan(items=list(entity_items.values()))


__all__ = ["CategoryRepository", "IncomeRepository", ""]
