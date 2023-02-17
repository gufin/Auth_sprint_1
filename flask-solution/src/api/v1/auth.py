from datetime import timedelta
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_pydantic import validate
from werkzeug.security import generate_password_hash

from api.v1.models import History, PasswordChange, UserBase
from core.settings import get_settings
from db.db_init import get_db
from db.redis import redis_db
from models.users import User, UserHistory

db = get_db()
auth = Blueprint("auth", __name__)
settings = get_settings()


@auth.route("/signup", methods=["POST"])
def signup():
    user = UserBase(**request.get_json())
    if db.session.query(User).filter(User.login == user.login).first():
        return {"msg": "User already exist"}, HTTPStatus.CONFLICT
    new_user = User(login=user.login)
    new_user.set_password(user.password)
    db.session.add(new_user)
    db.session.commit()
    return {"msg": "User was created."}, HTTPStatus.CREATED


@auth.route("/login", methods=["POST"])
@validate()
def login_user(body: UserBase):
    if user := db.session.query(User).filter(User.login == body.login).first():
        user_id = str(user.id)
        user_agent = request.headers.get("user-agent", "")
        user_host = request.headers.get("host", "")
        user_info = UserHistory(
            user_id=user_id,
            user_agent=user_agent,
            ip_address=user_host,
        )
        if user.check_password(body.password):
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(
                    seconds=settings.access_token_lifetime
                ),
                additional_claims={"is_administrator": user.is_superuser},
            )
            refresh_token = create_refresh_token(
                identity=user.id,
                expires_delta=timedelta(
                    seconds=settings.refresh_token_lifetime
                ),
            )

            db.session.add(user_info)
            db.session.commit()
            db.session.remove()
            redis_db.set(user_id, refresh_token)
            redis_db.expire(user_id, settings.refresh_token_lifetime)
            return jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            )
        return jsonify({"message": "Wrong password"}), HTTPStatus.CONFLICT
    return jsonify({"message": "Login not found"}), HTTPStatus.CONFLICT


@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    redis_db.set(jti, "")
    identity = get_jwt_identity()
    redis_db.delete(identity)
    return {"msg": "Access token revoked"}


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    try:
        refresh_token = request.headers.environ.get(
            "HTTP_AUTHORIZATION"
        ).replace("Bearer ", "")
    except Exception:
        return {"msg": "Failed to receive refresh token"}
    identity = get_jwt_identity()
    current_refresh_token = redis_db.get(identity)
    if current_refresh_token and current_refresh_token == refresh_token:
        access_token = create_access_token(
            identity=identity,
            expires_delta=timedelta(seconds=settings.access_token_lifetime),
        )
        refresh_token = create_refresh_token(
            identity=identity,
            expires_delta=timedelta(seconds=settings.refresh_token_lifetime),
        )
        redis_db.set(identity, refresh_token)
        redis_db.expire(identity, settings.refresh_token_lifetime)
        return jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )
    return {"msg": "Invalid token"}, HTTPStatus.CONFLICT


@auth.route("/change-password", methods=["PATCH"])
@validate()
@jwt_required()
def change_password(body: PasswordChange):
    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    if user is None:
        return {"message": "User not found"}

    if user.check_password(body.old_password):
        new_password = generate_password_hash(body.new_password)
        db.session.query(User).filter_by(id=user.id).update(
            {"password": new_password}
        )
        db.session.commit()
        return {"msg": "Password changed successfully"}

    return {"msg": "You entered the wrong old password"}, HTTPStatus.OK


@auth.route("/history", methods=["GET"])
@jwt_required()
@validate(response_many=True)
def get_history():
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    identity = get_jwt_identity()
    history = UserHistory.query.filter_by(user_id=identity).paginate(
        page=page, per_page=page_size
    )
    return [
        History(
            user_agent=row.user_agent,
            ip_address=row.ip_address,
            auth_datetime=row.auth_datetime,
        )
        for row in history.items
    ]
