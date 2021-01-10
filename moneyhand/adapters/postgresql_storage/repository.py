from contextvars import ContextVar
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import sql
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import (
    AsyncSessionTransaction,
)

from moneyhand.core import entities
from moneyhand.core.repository import AbstractUserRepository
from moneyhand.core.repository import AbstractTenantRepository
from moneyhand.core.repository import AbstractCategoryRepository
from moneyhand.core.repository import AbstractIncomeRepository
from moneyhand.core.repository import AbstractSpendingPlanRepository
from moneyhand.adapters.postgresql_storage import orm, helpers


class BaseAlchemyRepository:
    def __init__(self, uow_context_cv: ContextVar):
        self._context_cv = uow_context_cv

    @property
    def _transaction(self) -> AsyncSessionTransaction:
        return self._context_cv.get().session

    async def _upsert_row(self, row_class: orm.Base, _set_row_attributes, entity):
        res = await self._transaction.execute(
            select(row_class).filter(row_class.id == str(entity.id)).limit(1)
        )
        row = res.scalar()
        if row is None:
            row = row_class()

        _set_row_attributes(row, entity)
        return row


class TenantRepository(BaseAlchemyRepository, AbstractTenantRepository):
    async def save(self, tenant: entities.Tenant) -> None:
        row = await self._upsert_row(orm.Tenant, self._set_row_attributes, tenant)
        self._transaction.add(row)

    async def get(self, pk: UUID) -> Optional[entities.Tenant]:
        res = (
            await self._transaction.execute(
                select(orm.Tenant).filter(orm.Tenant.id == str(pk)).limit(1)
            )
        ).scalar()
        if res is None:
            return None

        return self._row_to_entity(res)

    @staticmethod
    def _row_to_entity(row: orm.Tenant) -> entities.Tenant:
        return entities.Tenant(id=UUID(row.id))

    @staticmethod
    def _set_row_attributes(sa_row: orm.Tenant, tenant: entities.Tenant) -> None:
        sa_row.id = str(tenant.id)


class UserRepository(BaseAlchemyRepository, AbstractUserRepository):
    async def save(self, user: entities.User) -> None:
        row = await self._upsert_row(orm.User, self._set_row_attributes, user)
        self._transaction.add(row)

        user_tenant_link: orm.TenantUser = (
            await self._transaction.execute(
                select(orm.TenantUser).filter(orm.TenantUser.user_id == str(user.id))
            )
        ).scalar()

        if user_tenant_link is not None:
            user_tenant_link.tenant_id = user.tenant_id
        else:
            self._transaction.add(
                orm.TenantUser(
                    id=str(uuid4()),
                    user_id=str(user.id),
                    tenant_id=str(user.tenant_id),
                )
            )

    async def get(self, pk: UUID) -> Optional[entities.User]:
        res = (
            await self._transaction.execute(
                select(orm.User).filter(orm.User.id == str(pk)).limit(1)
            )
        ).scalar()
        if res is None:
            return None

        return self._row_to_entity(res)

    async def find(self, name: str) -> Optional[entities.User]:
        res = (
            await self._transaction.execute(
                select(orm.User).filter(orm.User.name == name)
            )
        ).scalar()

        if res is None:
            return None

        return self._row_to_entity(res)

    @staticmethod
    def _row_to_entity(row: orm.User) -> entities.User:
        user = entities.User(
            id=UUID(row.id), name=row.name, email=row.email, disabled=row.disabled
        )
        user._password_hash = row.password_hash
        return user

    @staticmethod
    def _set_row_attributes(sa_row: orm.Category, user: entities.User) -> None:
        sa_row.id = str(user.id)
        sa_row.name = user.name
        sa_row.email = user.email
        sa_row.disabled = user.disabled
        sa_row.password_hash = user._password_hash


class CategoryRepository(BaseAlchemyRepository, AbstractCategoryRepository):
    async def get(self, pk: UUID) -> Optional[entities.Category]:
        res = (
            await self._transaction.execute(
                select(orm.Category).filter(orm.Category.id == str(pk)).limit(1)
            )
        ).scalar()
        if res is None:
            return None

        return self._row_to_entity(res)

    async def find(self, name: str) -> Optional[entities.Category]:
        res = await self._transaction.execute(
            select(orm.Category).filter(orm.Category.name == name)
        )
        return self._row_to_entity(res.scalar())

    async def save(self, category: entities.Category) -> None:
        row = await self._upsert_row(orm.Category, self._set_row_attributes, category)
        self._transaction.add(row)

    async def list(self) -> List[entities.Category]:
        res = await self._transaction.execute(select(orm.Category))
        return [self._row_to_entity(row) for row in res.scalars()]

    @staticmethod
    def _row_to_entity(
        row: orm.Category,
    ) -> entities.Category:
        return entities.Category(
            id=UUID(row.id), name=row.name, type=entities.CategoryType(row.type)
        )

    @staticmethod
    def _set_row_attributes(sa_row: orm.Category, category: entities.Category) -> None:
        sa_row.id = str(category.id)
        sa_row.name = category.name
        sa_row.type = category.type


class IncomeRepository(BaseAlchemyRepository, AbstractIncomeRepository):
    async def save(self, income: entities.Income) -> None:
        row = await self._upsert_row(orm.Income, self._set_row_attributes, income)
        self._transaction.add(row)

        await self._transaction.execute(
            delete(orm.IncomeItem).filter(orm.IncomeItem.income_id == str(income.id))
        )

        for i in (1, 2):
            self._transaction.add(
                orm.IncomeItem(
                    id=str(entities.new_id()),
                    income_id=str(income.id),
                    seq=i,
                    amount=getattr(income, f"part_{i}"),
                )
            )

    async def get(self) -> Optional[entities.Income]:
        table = orm.Income.__table__
        item_table = orm.IncomeItem.__table__

        res = (
            await self._transaction.execute(
                sql.select(
                    table.c.id,
                    table.c.is_template,
                    helpers.jsonb_agg(
                        helpers.json_build_object(
                            helpers.s("seq"),
                            item_table.c.seq,
                            helpers.s("amount"),
                            item_table.c.amount,
                        )
                    ).label("items"),
                )
                .join(item_table)
                .group_by(table.c.id)
            )
        ).first()

        if res is None:
            return None

        income = entities.Income(
            id=res.id,
            is_template=res.is_template,
        )

        for item in res.items:
            income.set_for(item["seq"], item["amount"])

        return income

    @staticmethod
    def _set_row_attributes(sa_row: orm.Income, income: entities.Income) -> None:
        sa_row.id = str(income.id)
        sa_row.is_template = income.is_template


class SpendingPlanRepository(BaseAlchemyRepository, AbstractSpendingPlanRepository):
    async def save(self, plan: entities.SpendingPlan) -> None:
        row = await self._upsert_row(orm.SpendingPlan, self._set_row_attributes, plan)

        self._transaction.add(row)

        await self._transaction.execute(
            delete(orm.SpendingPlanItem).filter(
                orm.SpendingPlanItem.spending_plan_id == str(plan.id)
            )
        )

        for item in plan.items:
            self._transaction.add(
                orm.SpendingPlanItem(
                    id=str(entities.new_id()),
                    spending_plan_id=str(plan.id),
                    category_id=str(item.category_id),
                    seq_num=1,
                    amount=item.part_1,
                )
            )
            self._transaction.add(
                orm.SpendingPlanItem(
                    id=str(entities.new_id()),
                    spending_plan_id=str(plan.id),
                    category_id=str(item.category_id),
                    seq_num=2,
                    amount=item.part_2,
                )
            )

    async def get(self, pk: UUID) -> Optional[entities.SpendingPlan]:
        table = orm.SpendingPlan.__table__
        item_table = orm.SpendingPlanItem.__table__

        query = (
            sql.select(
                table.c.id,
                table.c.is_template,
                helpers.jsonb_agg(
                    helpers.json_build_object(
                        helpers.s("category_id"),
                        item_table.c.category_id,
                        helpers.s("seq"),
                        item_table.c.seq_num,
                        helpers.s("amount"),
                        item_table.c.amount,
                    )
                ).label("items"),
            ).filter(
                table.c.id == pk
            )
            .outerjoin(item_table)
            .group_by(
                table.c.id,
            )
        )

        res = (await self._transaction.execute(query)).first()

        if res is None:
            return None

        plan = entities.SpendingPlan(id=res.id, is_template=res.is_template)

        for item in res.items:
            if item["category_id"] is None:
                continue

            plan.set_for_category(
                UUID(item["category_id"]), item["seq"], float(item["amount"])
            )

        return plan

    @staticmethod
    def _set_row_attributes(
        sa_row: orm.SpendingPlan,
        item: entities.SpendingPlan,
    ) -> None:
        sa_row.id = str(item.id)
        sa_row.is_template = item.is_template


__all__ = [
    "UserRepository",
    "TenantRepository",
    "CategoryRepository",
    "IncomeRepository",
    "SpendingPlanRepository",
]
