from uuid import UUID, uuid4
from pydantic import BaseModel, Field, PrivateAttr, validator

Model = BaseModel

CURRENCY_RUB = "RUB"


def new_id() -> UUID:
    return uuid4()
