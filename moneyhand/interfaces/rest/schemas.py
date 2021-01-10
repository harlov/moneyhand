from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from moneyhand.core import entities


class DumpCategory(BaseModel):
    id: UUID
    name: str
    type: entities.CategoryType


class CreateCategoryData(BaseModel):
    name: str
    type: entities.CategoryType


class UpdateCategoryData(BaseModel):
    name: Optional[str] = None
    type: Optional[entities.CategoryType] = None


class DumpIncome(BaseModel):
    part_1: Optional[float] = 0.0
    part_2: Optional[float] = 0.0


class UpdateIncomeData(BaseModel):
    part_1: Optional[float] = None
    part_2: Optional[float] = None


class DumpSpendingPlanItem:
    category_id: UUID
    part_1: float
    part_2: float


class DumpSpendingPlan(BaseModel):
    id: UUID
    items: List[dict]
