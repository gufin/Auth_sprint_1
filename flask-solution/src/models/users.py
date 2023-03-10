import uuid
from datetime import datetime
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from db.db_init import get_db
from core.settings import get_settings
from models.additions.partition import get_create_users_partitions_cmds

settings = get_settings()

db = get_db()


def create_partitions(target, connection, **kw):
    for cmd in get_create_users_partitions_cmds(
        settings.DB_USERS_PARTITIONS_NUM
    ):
        connection.execute(cmd)


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
    __table_args__ = {
        "postgresql_partition_by": "HASH (id)",
        "listeners": [("after_create", create_partitions)],
    }
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, unique=False, default=False)
    roles = db.relationship(
        "Role", secondary="users_roles", back_populates="users"
    )

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
    users = db.relationship(
        "User", secondary="users_roles", back_populates="roles"
    )

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
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    user_agent = db.Column(db.String, nullable=True)
    ip_address = db.Column(db.String, nullable=True)
    auth_datetime = db.Column(
        db.DateTime, default=datetime.now, nullable=False
    )

    def __repr__(self):
        return f"UserHistory: {self.user_agent} - {self.auth_datetime}"


class SocialAccount(db.Model):
    __tablename__ = "social_account"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    user = db.relationship(
        User, backref=db.backref("social_accounts", lazy=True)
    )

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
