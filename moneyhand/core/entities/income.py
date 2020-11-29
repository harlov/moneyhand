from uuid import UUID

from .base import Model, Field, CURRENCY_RUB

from moneyhand.core.errors import EntityValidationError


class Income(Model):
    id: UUID
    is_template: bool
    part_1: float = Field(default=0.0, ge=0.0)
    part_2: float = Field(default=0.0, ge=0.0)

    @property
    def currency(self) -> str:
        return CURRENCY_RUB

    def set_for(self, part: int, amount: float) -> None:
        if not (3 > part > 0):
            raise EntityValidationError("part", "must be between 1 and 2")

        attr_name = f"part_{part}"
        setattr(self, attr_name, amount)

    @property
    def total(self):
        return self.part_1 + self.part_2
