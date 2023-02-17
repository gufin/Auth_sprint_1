import os

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: int = os.getenv("REDIS_PORT", 6379)

    auth_service_host = os.getenv("AUTH_SERVICE_HOST", "auth_service")
    auth_service_port = os.getenv("AUTH_SERVICE_PORT", 5500)

    CONNECTIONS_MAX_TIME = 60

    class Config:
        env_file = ".env"


app_settings = AppSettings()
