import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    AUTH_PORT: int = 5500
    SECRET_KEY: str
    AUTH_HASH_METHOD: str
    AUTH_HASH_SALT_LENGTH: int
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DevSettings(Settings):
    FLASK_ENV: str = 'development'
    DEBUG: bool = True
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return DevSettings()
