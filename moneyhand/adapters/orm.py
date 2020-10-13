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
