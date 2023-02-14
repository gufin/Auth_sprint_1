from flask import Flask
from db.db_init import create_db


def create_app(config_filename: object) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.app_context().push()
    create_db(app)
    return app