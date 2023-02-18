from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from db.db_init import create_db


def create_app(config_filename: object) -> Flask:
    app = Flask(__name__)
    swagger = Swagger(app, template_file="docs/openapi.yaml")
    jwt = JWTManager(app)
    app.config.from_object(config_filename)
    app.app_context().push()
    create_db(app)
    from api.v1.auth import auth
    from api.v1.roles import roles
    from api.v1.user_roles import users
    from createsuperuser import superuser_pb

    app.register_blueprint(auth, url_prefix="/api/v1/auth")
    app.register_blueprint(roles, url_prefix="/api/v1/roles")
    app.register_blueprint(users, url_prefix="/api/v1/users")
    app.register_blueprint(superuser_pb)

    return app
