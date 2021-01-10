from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork
from .core.service import Service


def create_service() -> Service:
    uow = UnitOfWork()
    service = Service(uow=uow)
    return service
