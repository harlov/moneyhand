from __future__ import annotations

import enum

from typing import Optional, List
from uuid import UUID
from uuid import uuid4
from pydantic import BaseModel, Field, validators
from pydantic import validator


def new_id() -> UUID:
    return uuid4()


CURRENCY_RUB = "RUB"


class CategoryType(enum.IntEnum):
    NECESSARY = enum.auto()
    GOAL = enum.auto()


class Category(BaseModel):
    id: UUID
    name: str
    type: CategoryType

    @validator("name")
    def name_must_be_not_empty(cls, name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError("must be not empty")

        return name


class Income(BaseModel):
    id: UUID
    is_template: bool
    part_1: float = Field(default=0.0, ge=0.0)
    part_2: float = Field(default=0.0, ge=0.0)

    @property
    def currency(self) -> str:
        return CURRENCY_RUB

    def set_for(self, part: int, amount: float) -> None:
        if not (3 > part > 0):
            raise ValueError("must be between 1 and 2")

        attr_name = f"part_{part}"
        setattr(self, attr_name, amount)

    @property
    def total(self):
        return self.part_1 + self.part_2


class SpendingPlanItem(BaseModel):
    category_id: UUID
    part_1: Optional[float] = 0.0
    part_2: Optional[float] = 0.0

    @property
    def total(self):
        return self.part_1 + self.part_2

    @property
    def currency(self):
        return CURRENCY_RUB

    def set_for(self, part: int, amount: float) -> None:
        if not (3 > part > 0):
            raise ValueError("must be between 1 and 2")

        attr_name = f"part_{part}"
        setattr(self, attr_name, amount)


class SpendingPlan(BaseModel):
    id: UUID
    is_template: bool
    items: List[SpendingPlanItem] = Field(default_factory=list)

    def set_for_category(self, category_id: UUID, part: int, amount: float) -> None:
        target_item: SpendingPlanItem

        for item in self.items:
            if item.category_id == category_id:
                target_item = item
                break
        else:
            target_item = SpendingPlanItem(category_id=category_id)
            self.items.append(target_item)

        target_item.set_for(part, amount)

    @property
    def total_part_1(self) -> float:
        return sum((item.part_1 for item in self.items))

    @property
    def total_part_2(self) -> float:
        return sum((item.part_2 for item in self.items))


class BalanceReport(BaseModel):
    part_1: float
    part_2: float

    @property
    def currency(self) -> str:
        return CURRENCY_RUB

    @classmethod
    def create(cls, income: Income, spending_plan: SpendingPlan) -> BalanceReport:
        return BalanceReport(
            part_1=income.part_1 - spending_plan.total_part_1,
            part_2=income.part_2 - spending_plan.total_part_2,
        )
