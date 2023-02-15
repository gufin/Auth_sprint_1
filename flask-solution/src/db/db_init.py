from typing import Optional

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db: Optional[SQLAlchemy] = None


def create_db(app: Flask):
    """initialize db for SQLAlchemy."""
    global db
    db = SQLAlchemy(app)
    Migrate(app, db)


def get_db() -> SQLAlchemy:
    return db
