import pytest

from moneyhand.core.service import Service


@pytest.fixture
def service_in_memory(unit_of_work_memory) -> Service:
    return Service(uow=unit_of_work_memory)
