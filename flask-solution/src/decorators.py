from functools import wraps
from flask_jwt_extended import get_jwt_identity
from http import HTTPStatus


def jwt_roles_accepted(model, *roles: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user_id = get_jwt_identity()
            user = model.query.filter_by(id=user_id).first()
            if not user or not user.roles:
                return {"msg": "Доступ запрещен."}, HTTPStatus.FORBIDDEN
            return (
                fn(*args, **kwargs)
                if {role.name for role in user.roles}.intersection(roles)
                else ({"msg": "Доступ запрещен."}, HTTPStatus.FORBIDDEN)
            )

        return decorated_view

    return wrapper
