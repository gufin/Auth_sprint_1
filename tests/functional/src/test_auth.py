import requests
from mimesis import Person

from conftest import HOST


def test_signup_valid_data():
    user = Person()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f"{HOST}/api/v1/auth/signup"
    data = {"login": user.email(unique=True), "password": user.password()}
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == 201


def test_signup_invalid_data(signup):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = f"{HOST}/api/v1/auth/signup"
    data = {"login": signup.get("login"), "password": signup.get("password")}
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == 409


def test_signin_valid_data(signup):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {"login": signup.get("login"), "password": signup.get("password")}
    url = f"{HOST}/api/v1/auth/login"
    response = requests.post(url=url, json=data, headers=headers)
    assert "access_token" in response.json()


def test_signin_invalid_data(signup):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {"login": signup.get("login"), "password": "123"}
    url = f"{HOST}/api/v1/auth/login"
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == 409


def test_logout(login):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login.get('access_token')}",
    }
    url = f"{HOST}/api/v1/auth/logout"
    response = requests.post(url=url, headers=headers)
    assert response.status_code == 200


def test_refresh_revoked_after_logout(login):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login.get('access_token')}",
    }
    url = f"{HOST}/api/v1/auth/logout"
    requests.post(url=url, headers=headers)

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login.get('refresh_token')}",
    }
    url = f"{HOST}/api/v1/auth/refresh"
    response = requests.post(url=url, headers=headers)
    assert response.status_code == 409


def test_change_password(login):
    user = Person()
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login.get('access_token')}",
    }
    url = f"{HOST}/api/v1/auth/change-password"
    new_pass = user.password()
    data = {"old_password": "test", "new_password": new_pass}
    response = requests.patch(url=url, headers=headers, json=data)

    data_rollback = {"old_password": new_pass, "new_password": "test"}
    response_rollback = requests.patch(
        url=url, headers=headers, json=data_rollback
    )
    assert response.status_code == 200
    assert response_rollback.status_code == 200


def test_get_refresh(login):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login.get('refresh_token')}",
    }
    url = f"{HOST}/api/v1/auth/refresh"
    response = requests.post(url=url, headers=headers)
    assert response.status_code == 200


def test_history(login):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login.get('access_token')}",
    }
    url = f"{HOST}/api/v1/auth/history"
    response = requests.get(url=url, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 1
