import enum
from uuid import UUID

from .base import Model, validator


class CategoryType(enum.IntEnum):
    NECESSARY = enum.auto()
    GOAL = enum.auto()


class Category(Model):
    id: UUID
    name: str
    type: CategoryType

    @validator("name")
    def name_must_be_not_empty(cls, name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError("must be not empty")

        return name
