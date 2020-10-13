from dataclasses import dataclass
from uuid import UUID
from uuid import uuid4


def new_id() -> UUID:
    return uuid4()


@dataclass
class Category:
    id: UUID
    name: str
