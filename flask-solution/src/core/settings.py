import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    AUTH_PORT: int = 5500

    AUTH_HASH_METHOD: str = os.getenv("AUTH_HASH_METHOD")
    AUTH_HASH_SALT_LENGTH: int = os.getenv("AUTH_HASH_SALT_LENGTH")
    access_token_lifetime: int = 600
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_USERS_PARTITIONS_NUM: int = 8
    refresh_token_lifetime: int = 3600
    REQUEST_LIMIT_PER_MINUTE: int = 20
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    TRACER_ENABLED: bool = os.getenv('TRACER_ENABLED', False)
    TRACER_HOST: str = 'jaeger'
    TRACER_PORT: int = 6831
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    OAUTH_CREDENTIALS = {
        "yandex": {
            "client_id": os.getenv("YANDEX_OAUTH_ID"),
            "client_secret": os.getenv("YANDEX_OAUTH_SECRET"),
            "authorize_url": "https://oauth.yandex.ru/authorize",
            "access_token_url": "https://oauth.yandex.ru/token",
            "base_url": "https://login.yandex.ru/",
        },
        "google": {
            "client_id": os.getenv("GOOGLE_OAUTH_ID"),
            "client_secret": os.getenv("GOOGLE_OAUTH_SECRET"),
            "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            "access_token_url": "https://accounts.google.com/o/oauth2/token",
            "base_url": "https://www.googleapis.com/plus/v1/people/",
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
