from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork
from .core.service import Service


async def create_service() -> Service:
    uow = UnitOfWork()
    await uow.setup()
    service = Service(uow=uow)
    return service
