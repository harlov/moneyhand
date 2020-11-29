from uuid import UUID


class BaseError(Exception):
    pass


class EntityNotFound(BaseError):
    entity_name: str
    pk: UUID

    def __init__(self, entity_name: str, pk: UUID):
        self.entity_name = entity_name
        self.pk = pk


class EntityValidationError(Exception):
    def __init__(self, field, error):
        self.field = field
        self.error = error


class AuthCredentialsInvalidError(Exception):
    pass
