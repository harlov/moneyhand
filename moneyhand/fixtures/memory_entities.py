import pytest

from moneyhand.core.entities import Tenant, User
from moneyhand.core.unit_of_work import AbstractUnitOfWork


@pytest.fixture
async def mem_tenant(tenant: Tenant, unit_of_work_memory: AbstractUnitOfWork):
    async with unit_of_work_memory:
        await unit_of_work_memory.tenant.save(tenant)

    return tenant


@pytest.fixture
async def mem_user(user: User, unit_of_work_memory: AbstractUnitOfWork):
    async with unit_of_work_memory:
        await unit_of_work_memory.user.save(user)

    return user
