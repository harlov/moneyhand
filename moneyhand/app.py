from .adapters.unit_of_work import UnitOfWork
from .core.service import Service
from .interfaces.rest import RESTInterface


async def create_service() -> Service:
    uow = UnitOfWork()
    await uow.setup()
    service = Service(uow=uow)
    return service
