from http import HTTPStatus
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate

from api.v1.models import RoleUser, RoleBase
from decorators import jwt_roles_accepted
from core.rate_limiter import rate_limit
from models.users import UserRole, User
from db.db_init import get_db

db = get_db()

users = Blueprint("users", __name__)


@users.route("/", methods=["GET"])
@rate_limit()
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def users_list():
    return [{user.login: str(user.id)} for user in User.query.all()]


@users.route("/roles", methods=["GET"])
@rate_limit()
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate(response_many=True)
def get_user_roles():
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    if user is None:
        return {"message": "User not found. Check uuid"}, HTTPStatus.NOT_FOUND
    return [RoleBase(name=role.name) for role in user.roles]


@users.route("/assign-role", methods=["POST"])
@rate_limit()
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def assign_roles(body: RoleUser):
    if (
        db.session.query(UserRole)
        .filter(
            UserRole.user_id == body.user_id, UserRole.role_id == body.role_id
        )
        .first()
    ):
        return {
            "msg": "Role is already assigned to the user"
        }, HTTPStatus.BAD_REQUEST
    new_role_user = UserRole(user_id=body.user_id, role_id=body.role_id)

    db.session.add(new_role_user)
    db.session.commit()
    return {"msg": "Role is assigned to the user"}, HTTPStatus.CREATED


@users.route("/delete-role", methods=["DELETE"])
@rate_limit()
@jwt_required()
@jwt_roles_accepted(User, "admin")
@validate()
def delete_role_from_user(body: RoleUser):
    role_user = (
        db.session.query(UserRole)
        .filter(
            UserRole.user_id == body.user_id, UserRole.role_id == body.role_id
        )
        .first()
    )
    if not role_user:
        return {"msg": "Role for user not found"}, HTTPStatus.NOT_FOUND
    db.session.query(UserRole).filter_by(
        user_id=body.user_id, role_id=body.role_id
    ).delete()
    db.session.commit()
    return {"msg": "Role for user successfully deleted"}, HTTPStatus.OK
