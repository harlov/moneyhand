import pytest

from moneyhand.adapters.postgresql_storage.unit_of_work import UnitOfWork
from moneyhand.core.entities import new_id
from moneyhand.core.entities import Tenant

pytestmark = pytest.mark.asyncio


async def test_get(unit_of_work_pg: UnitOfWork, pg_tenant: Tenant):
    async with unit_of_work_pg:
        tenant = await unit_of_work_pg.tenant.get(pg_tenant.id)

    assert tenant == pg_tenant


async def test_get_not_exists(unit_of_work_pg: UnitOfWork):
    async with unit_of_work_pg:
        tenant = await unit_of_work_pg.tenant.get(new_id())

    assert tenant is None


async def test_create(unit_of_work_pg: UnitOfWork, pg_tenant: Tenant):
    async with unit_of_work_pg:
        new_tenant = Tenant(id=new_id())
        await unit_of_work_pg.tenant.save(new_tenant)

    async with unit_of_work_pg:
        new_tenant_refreshed = await unit_of_work_pg.tenant.get(new_tenant.id)
        assert new_tenant_refreshed == new_tenant
