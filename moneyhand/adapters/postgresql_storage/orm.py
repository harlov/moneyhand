from typing import Any

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

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


class Income(Base):
    __tablename__ = "incomes"
    id = ID()
    seq_num = sa.Column(sa.Integer)
    amount = sa.Column(sa.Float)


class SpendingPlanItem(Base):
    __tablename__ = "spending_plan_items"

    id = ID()
    category_id = sa.Column(pg.UUID())
    seq_num = sa.Column(sa.Integer)
    amount = sa.Column(sa.Float)
