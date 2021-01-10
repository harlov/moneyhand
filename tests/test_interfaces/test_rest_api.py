import pytest

from uuid import uuid4

from moneyhand.core import entities
from moneyhand.core.service import Service
from moneyhand.interfaces import rest
from fastapi.testclient import TestClient


@pytest.fixture
def service_in_memory(unit_of_work_memory):
    return Service(unit_of_work_memory)


def fake_uuid_str():
    return str(uuid4())


@pytest.fixture
async def rest_client_unauthorized(monkeypatch, service_in_memory):
    monkeypatch.setattr(rest, "service", service_in_memory, raising=False)
    monkeypatch.setattr(rest.security, "service", service_in_memory, raising=False)
    return TestClient(rest.app)


@pytest.fixture
async def rest_client(monkeypatch, service_in_memory, mem_user: entities.User):
    monkeypatch.setattr(rest, "service", service_in_memory, raising=False)
    monkeypatch.setattr(rest.security, "service", service_in_memory, raising=False)

    token = await service_in_memory.tenant.create_access_token("user", "password")
    c = TestClient(rest.app)
    c.headers.update({"Authorization": f"Bearer {token}"})
    return c


def test_login_and_get_info(rest_client_unauthorized, mem_user: entities.User):
    res_token = rest_client_unauthorized.post(
        "/user/token",
        data={
            "username": "user",
            "password": "password",
        },
    )

    assert res_token.status_code == 200
    token_json = res_token.json()
    assert list(token_json.keys()) == ["access_token", "token_type"]
    assert token_json["token_type"] == "bearer"

    res_info = rest_client_unauthorized.get(
        "/user", headers={"Authorization": f"Bearer {token_json['access_token']}"}
    )

    assert res_info.status_code == 200
    assert res_info.json() == {
        "id": str(mem_user.id),
        "name": mem_user.name,
        "email": mem_user.email,
        "telegram_link": mem_user.telegram_link,
        "disabled": mem_user.disabled,
    }


@pytest.mark.parametrize(
    "route, verb",
    [
        ("/user", "GET"),
        ("/categories", "GET"),
        ("/categories", "POST"),
        (f"/categories/{fake_uuid_str()}", "PATCH"),
        ("/income", "GET"),
        ("/income", "PATCH"),
    ],
)
def test_unauthorized(rest_client_unauthorized, route, verb):
    method = getattr(rest_client_unauthorized, verb.lower())
    res = method(route)

    assert res.status_code == 401


def test_create_category(rest_client):
    res = rest_client.post("/categories", json={"name": "Rent", "type": 2})
    assert res.status_code == 200
    res_json = res.json()

    res_json.pop("id")
    assert res_json == {"name": "Rent", "type": 2}


def test_update_category_name(rest_client, mem_category_food: entities.Category):
    res = rest_client.patch(
        f"/categories/{mem_category_food.id}", json={"name": "FastFood"}
    )

    assert res.status_code == 200
    assert res.json() == {
        "id": str(mem_category_food.id),
        "name": "FastFood",
        "type": entities.CategoryType.NECESSARY.value,
    }


def test_update_category_type(rest_client, mem_category_food: entities.Category):
    res = rest_client.patch(
        f"/categories/{mem_category_food.id}",
        json={"type": entities.CategoryType.GOAL.value},
    )

    assert res.status_code == 200
    assert res.json() == {
        "id": str(mem_category_food.id),
        "name": "Food",
        "type": entities.CategoryType.GOAL.value,
    }


def test_update_unknown_category(rest_client):
    pk = fake_uuid_str()
    res = rest_client.patch(f"/categories/{pk}", json={"name": "smth"})

    assert res.status_code == 404
    assert res.json() == {"error": "not_found", "entity": "category", "pk": str(pk)}


def test_get_income(rest_client, mem_income: entities.Income):
    res = rest_client.get(f"/income")
    assert res.status_code == 200
    assert res.json() == {"part_1": mem_income.part_1, "part_2": mem_income.part_2}


def test_set_income(rest_client, mem_income: entities.Income):
    res = rest_client.patch(f"/income", json={"part_1": 10000})
    assert res.status_code == 200
    assert res.json() == {"part_1": 10000, "part_2": mem_income.part_2}
