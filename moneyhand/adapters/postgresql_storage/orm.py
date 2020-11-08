from typing import Any

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ID(sa.Column):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            **dict(
                kwargs,
                name="id",
                type_=pg.UUID,
                primary_key=True,
            )
        )


class Category(Base):
    __tablename__ = "categories"

    id = ID()
    name = sa.Column(sa.String)
    type = sa.Column(sa.Integer)


class Income(Base):
    __tablename__ = "incomes"
    id = ID()
    is_template = sa.Column(sa.Boolean)


class IncomeItem(Base):
    __tablename__ = "income_items"
    id = ID()
    income_id = sa.Column(pg.UUID(), sa.ForeignKey("incomes.id"))
    seq = sa.Column(sa.Integer)
    amount = sa.Column(sa.Float)


class SpendingPlan(Base):
    __tablename__ = "spending_plans"
    id = ID()
    is_template = sa.Column(sa.Boolean)


class SpendingPlanItem(Base):
    __tablename__ = "spending_plan_items"

    id = ID()
    spending_plan_id = sa.Column(
        pg.UUID(), sa.ForeignKey("spending_plans.id", deferrable=True)
    )
    category_id = sa.Column(pg.UUID())
    seq_num = sa.Column(sa.Integer)
    amount = sa.Column(sa.Float)
