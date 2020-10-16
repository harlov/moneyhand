from typing import Optional
from uuid import UUID
from uuid import uuid4
from pydantic import BaseModel, Field
from pydantic import validator


def new_id() -> UUID:
    return uuid4()


class Category(BaseModel):
    id: UUID
    name: str


class IncomePart(BaseModel):
    id: Optional[UUID] = Field(default_factory=new_id)
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
        return "RUB."

    def set_for(self, part: int, amount: float) -> None:
        if not (3 > part > 0):
            raise ValueError("must be between 1 and 2")

        attr_name = f"part_{part}"
        setattr(self, attr_name, IncomePart(amount=amount))

    @property
    def total(self):
        return self.part_1.amount + self.part_2.amount

    def __str__(self):
        return f"""
        Income:
            part 1: {self.part_1.amount} {self.currency}.
            part 2: {self.part_2.amount} {self.currency}.
        ---
        Total: {self.part_1.amount + self.part_2.amount} {self.currency}.
        """
