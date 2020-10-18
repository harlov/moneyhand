from uuid import UUID


class BaseError(Exception):
    pass


class EntityNotFound(BaseError):
    entity_name: str
    pk: UUID

    def __init__(self, entity_name: str, pk: UUID):
        self.entity_name = entity_name
        self.pk = pk
