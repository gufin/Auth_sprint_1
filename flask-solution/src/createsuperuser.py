from http import HTTPStatus

import click
from flask import Blueprint

from db.db_init import get_db
from models.users import Role, User, UserRole

db = get_db()
superuser_pb = Blueprint("superuser", __name__)


@superuser_pb.cli.command("create")
@click.argument("login")
@click.argument("password")
@click.argument("email")
def createsuperuser(login, password, email):
    if (
        db.session.query(User)
        .filter((User.login == login) | (User.email == email))
        .first()
    ):
        return "User already exist. Try another login", HTTPStatus.BAD_REQUEST
    superuser = User(login=login, email=email, is_superuser=True)
    superuser.set_password(password)
    db.session.add(superuser)
    db.session.commit()
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    new_role_user = UserRole(user_id=superuser.id, role_id=role.id)
    db.session.add(new_role_user)
    db.session.commit()
    return "Superuser was created", HTTPStatus.CREATED
