from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from api.v1.auth import auth
from db.db import init_db

app = Flask(__name__)


def create_app():
    app = Flask(__name__)

    jwt = JWTManager(app)
    init_db(app)
    #db = SQLAlchemy(app)

    app.register_blueprint(auth, url_prefix="/api/v1/auth")

    return app


if __name__ == '__main__':
    create_app()