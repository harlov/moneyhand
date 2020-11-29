from pydantic import BaseModel
from moneyhand.core import entities


class CreateCategoryData(BaseModel):
    name: str
    type: entities.CategoryType
