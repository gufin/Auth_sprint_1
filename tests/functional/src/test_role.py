from http import HTTPStatus

import requests
import random
from mimesis import Person

from conftest import HOST
from utils.helpers import get_user_id, get_role_id

role_name = f"designer - {random.randint(1, 100)}"
role_id = None
user_login = f"user - {random.randint(1, 100)}"
user_id = None


def test_create_role_by_admin(login_admin):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/roles/create"
    data = {"name": role_name}
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED


def test_create_role_by_user(signup, login):
    mimerand = Person()
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login.get('access_token')}",
    }
    url = f"{HOST}/api/v1/roles/create"
    data = {"name": mimerand.political_views()}
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_show_roles(login_admin):
    global role_id
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/roles"
    response = requests.get(url=url, headers=headers)
    role_id = get_role_id(data=response.json(), role=role_name)
    assert response.status_code == HTTPStatus.OK


def test_update_role(login_admin):
    global role_name
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/roles/{role_id}"
    new_name = f"{role_name}_new"
    data = {"name": new_name}
    response = requests.patch(url=url, json=data, headers=headers)
    assert response.status_code == HTTPStatus.OK
    role_name = new_name


def test_show_users(login_admin):
    global user_id
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/users"
    response = requests.get(url=url, headers=headers)
    user_id = get_user_id(data=response.json(), user_name="admin")
    assert response.status_code == HTTPStatus.OK


def test_show_user_roles(login_admin):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/users/roles"
    response = requests.get(url=url, headers=headers)
    assert response.status_code == HTTPStatus.OK


def test_user_add_role(login_admin):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/users/assign-role"
    data = {
        "user_id": user_id,
        "role_id": role_id,
    }
    response = requests.post(url=url, json=data, headers=headers)
    assert response.status_code == HTTPStatus.CREATED


def test_user_role_remove(login_admin):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/users/delete-role"
    data = {"user_id": user_id, "role_id": role_id}
    response = requests.delete(url=url, json=data, headers=headers)
    assert response.status_code == HTTPStatus.OK


def test_delete_role(login_admin):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {login_admin.get('access_token')}",
    }
    url = f"{HOST}/api/v1/roles/{role_id}"
    response = requests.delete(url=url, headers=headers)
    assert response.status_code == HTTPStatus.OK
