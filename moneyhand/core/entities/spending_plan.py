from typing import Optional, List
from uuid import UUID

from .base import Model, Field, CURRENCY_RUB

from moneyhand.core.errors import EntityValidationError


class SpendingPlanItem(Model):
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
            raise EntityValidationError("part", "must be between 1 and 2")

        attr_name = f"part_{part}"
        setattr(self, attr_name, amount)


class SpendingPlan(Model):
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
