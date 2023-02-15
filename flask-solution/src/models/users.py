from datetime import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from db.db_init import get_db

db = get_db()


class UserRole(db.Model):
    __tablename__ = "users_roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        default=uuid.uuid4(),
        nullable=False,
    )
    role_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("roles.id"),
        default=uuid.uuid4(),
        nullable=False,
    )


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False)
    roles = db.relationship("Role", secondary="users_roles", back_populates="users")

    def __repr__(self):
        return f"<User {self.login}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    name = db.Column(db.String(32), unique=True, nullable=False)
    users = db.relationship("User", secondary="users_roles", back_populates="roles")

    def __repr__(self):
        return f"<Role {self.name}>"


class UserHistory(db.Model):
    __tablename__ = "user_history"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    user_agent = db.Column(db.String, nullable=True)
    ip_address = db.Column(db.String, nullable=True)
    auth_datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"UserHistory: {self.user_agent} - {self.auth_datetime}"
