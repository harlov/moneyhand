from __future__ import annotations

import typing

from .base import Model
from .base import CURRENCY_RUB

if typing.TYPE_CHECKING:
    from .income import Income
    from .spending_plan import SpendingPlan


class BalanceReport(Model):
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
