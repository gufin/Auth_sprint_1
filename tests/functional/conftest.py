import requests

import pytest
from settings import app_settings

HOST = (
    f"http://{app_settings.auth_service_host}:{app_settings.auth_service_port}"
)


@pytest.fixture()
def login() -> dict:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f"{HOST}/api/v1/auth/login"
    data = {"login": "gufinhaly", "password": "test"}
    response = requests.post(url=url, json=data, headers=headers)
    return dict(response.json())


@pytest.fixture()
def signup() -> dict:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f"{HOST}/api/v1/auth/signup"
    data = {
        "email": "gufinhaly@gmail.com",
        "password": "test",
        "login": "gufinhaly",
    }
    requests.post(url=url, json=data, headers=headers)
    return data


@pytest.fixture()
def login_admin() -> dict:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f"{HOST}/api/v1/auth/login"
    data = {"login": "admin", "password": "admin"}
    response = requests.post(url=url, json=data, headers=headers)
    return dict(response.json())
