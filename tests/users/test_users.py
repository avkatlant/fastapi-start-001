import json
from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient


async def test_get_users(client: AsyncClient) -> None:
    response = await client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    print(response.json())


users_data = [
    {"name": "sasha", "surname": "www", "email": "lol90@kek.com", "password": "eeee!"},
    {"name": "qqq", "surname": "eee", "email": "fsfdfdfsd0@kek.com", "password": "gdhfhfgh"},
]


@pytest.mark.parametrize("value", users_data, ids=str)
async def test_create_user(client: AsyncClient, value: dict[str, Any]) -> None:
    response = await client.post("/users/", content=json.dumps(value))
    assert response.status_code == status.HTTP_201_CREATED
    data_from_resp = response.json()
    assert data_from_resp["name"] == value["name"]
    assert data_from_resp["surname"] == value["surname"]
    assert data_from_resp["email"] == value["email"]
