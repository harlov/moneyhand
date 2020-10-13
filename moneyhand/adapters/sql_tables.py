from typing import Any

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


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


metadata = sa.MetaData()


categories = sa.Table(
    "categories",
    metadata,
    ID(),
    sa.Column("name", sa.String)
)
