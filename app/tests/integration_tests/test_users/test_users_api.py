import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "pes0kot", 200),
    ("abcde", "pes0kot", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    responce = await ac.post('/auth/register', json={
        "email": email,
        "password": password,
    })
    assert responce.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("wrong@example.com", "test", 401),
    ("abcde", "artem", 422)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    responce = await ac.post('/auth/login', json={
        "email": email,
        "password": password,
    })
    assert responce.status_code == status_code