import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    AUTH_PORT: int = 5500
    SECRET_KEY: str
    AUTH_HASH_METHOD: str
    AUTH_HASH_SALT_LENGTH: int
    access_token_lifetime: int = 600
    refresh_token_lifetime: int = 3600
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DevSettings(Settings):
    flask_env: str = "development"
    debug: bool = True
    testing: bool = True
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return DevSettings()
