import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    AUTH_PORT: int = 5500
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    AUTH_HASH_METHOD: str = os.getenv("AUTH_HASH_METHOD")
    AUTH_HASH_SALT_LENGTH: int = os.getenv("AUTH_HASH_SALT_LENGTH")
    access_token_lifetime: int = 600
    refresh_token_lifetime: int = 3600
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    REQUEST_LIMIT_PER_MINUTE: int = 20
    OAUTH_CREDENTIALS = {
        "yandex": {
            "client_id": os.getenv("YANDEX_OAUTH_ID"),
            "client_secret": os.getenv("YANDEX_OAUTH_SECRET"),
            "authorize_url": "https://oauth.yandex.ru/authorize",
            "access_token_url": "https://oauth.yandex.ru/token",
            "base_url": "https://login.yandex.ru/",
        },
    }

    class Config:
        env_file = ".env"


class DevSettings(Settings):
    flask_env: str = "development"
    debug: bool = True
    testing: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
