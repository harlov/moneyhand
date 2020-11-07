from __future__ import annotations

from typing import Optional, List
from uuid import UUID
from uuid import uuid4
from pydantic import BaseModel, Field
from pydantic import validator


def new_id() -> UUID:
    return uuid4()


CURRENCY_RUB = "RUB"


class Category(BaseModel):
    id: UUID
    name: str

    @validator("name")
    def name_must_be_not_empty(cls, name: str) -> str:
        name = name.strip()

        if not name:
            raise ValueError("must be not empty")

        return name


class IncomePart(BaseModel):
    amount: Optional[float] = 0.0

    @validator("amount")
    def amount_must_be_not_negative(cls, amount: int) -> int:
        # TODO: move into separated validators package
        if amount < 0:
            raise ValueError("must be not negative")
        return amount


class Income(BaseModel):
    part_1: Optional[IncomePart] = IncomePart()
    part_2: Optional[IncomePart] = IncomePart()

    @property
    def currency(self) -> str:
        return CURRENCY_RUB

    def set_for(self, part: int, amount: float) -> None:
        if not (3 > part > 0):
            raise ValueError("must be between 1 and 2")

        attr_name = f"part_{part}"
        setattr(self, attr_name, IncomePart(amount=amount))

    @property
    def total(self):
        return self.part_1.amount + self.part_2.amount


class SpendingPart(BaseModel):
    amount: Optional[float] = 0.0


class SpendingPlanItem(BaseModel):
    category_id: UUID
    part_1: Optional[SpendingPart] = SpendingPart()
    part_2: Optional[SpendingPart] = SpendingPart()

    @property
    def total(self):
        return self.part_1.amount + self.part_2.amount

    @property
    def currency(self):
        return CURRENCY_RUB

    def set_for(self, part: int, amount: float) -> None:
        if not (3 > part > 0):
            raise ValueError("must be between 1 and 2")

        attr_name = f"part_{part}"
        setattr(self, attr_name, SpendingPart(amount=amount))


class SpendingPlan(BaseModel):
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
        return sum((item.part_1.amount for item in self.items))

    @property
    def total_part_2(self) -> float:
        return sum((item.part_2.amount for item in self.items))


class BalanceReport(BaseModel):
    part_1: float
    part_2: float

    @classmethod
    def create(cls, income: Income, spending_plan: SpendingPlan) -> BalanceReport:
        return BalanceReport(
            part_1=income.part_1.amount - spending_plan.total_part_1,
            part_2=income.part_2.amount - spending_plan.total_part_2,
        )
