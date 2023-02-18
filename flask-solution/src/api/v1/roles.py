from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from pydantic import UUID4

from decorators import jwt_roles_accepted
from api.v1.models import RoleBase
from models.users import Role, User

from db.db_init import get_db

db = get_db()

roles = Blueprint("roles", __name__)


@roles.route("/", methods=["GET"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def roles_list():
    return [{role.name: str(role.id)} for role in Role.query.all()]


@roles.route("/create", methods=["POST"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def create_role(body: RoleBase):
    if db.session.query(Role).filter(Role.name == body.name).first():
        return {
            "msg": f"Role {body.name} already exist"
        }, HTTPStatus.BAD_REQUEST
    new_role = Role(name=body.name)
    db.session.add(new_role)
    db.session.commit()
    return {"msg": f"Role {new_role.name} was created"}, HTTPStatus.CREATED


@roles.route("/<role_id>", methods=["PATCH"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def update_role(role_id: UUID4, body: RoleBase):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
    if Role.query.filter_by(name=body.name).first():
        return {
            "msg": "Role with this name already exist"
        }, HTTPStatus.CONFLICT
    role.name = body.name
    db.session.query(Role).filter_by(id=role.id).update({"name": role.name})
    db.session.commit()
    updated_role = RoleBase(id=role.id, name=role.name)
    return {
        "msg": f"Name for the role was changed to {updated_role.name}"
    }, HTTPStatus.OK


@roles.route("/<role_id>", methods=["DELETE"])
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def delete_role(role_id: UUID4):
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return {"msg": "Role not found"}, HTTPStatus.NOT_FOUND
    db.session.query(Role).filter_by(id=role.id).delete()
    db.session.commit()
    return {"msg": f"Role {role.name} successfully deleted"}, HTTPStatus.OK
