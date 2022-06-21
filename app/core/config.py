import os
import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator


def assemble_value(v: Union[str, List[str]]) -> Union[List[str], str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], AnyHttpUrl] = []

    _assemble_cors_origin = validator("BACKEND_CORS_ORIGINS", allow_reuse=True)(assemble_value)

    PROJECT_NAME: str = "API TextStat"

    POSTGRES_HOSTNAME: str = "postgres"
    POSTGRES_PORT: str = 5432
    POSTGRES_USER: str = "test"
    POSTGRES_PASSWORD: str = "test"
    POSTGRES_DB: str = "test"

    SQLALCHEMY_DATABASE_URI: Optional[str]
    DATABASE_ENGINE_POOL_SIZE: Optional[int] = 20
    DATABASE_ENGINE_MAX_OVERFLOW: Optional[int] = 0

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        port = values.get('POSTGRES_PORT') or 5432
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOSTNAME"),
            port=str(port),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # FILE_CONTENT_TYPES: str = "text/plain"
    FILE_CONTENT_TYPES: Union[List[str], str] = ["text/plain"]
    FILE_OUT_PATH: str = os.path.abspath("files")

    _assemble_file_types = validator("FILE_CONTENT_TYPES", allow_reuse=True)(assemble_value)

    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_MAIN_QUEUE: str = "main-queue"
    CELERY_BROKER_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    CELERY_ACCEPT_CONTENT: Union[List[str], str] = ["application/json"]
    CELERY_TASK_SERIALIZER: str = "json"
    CREATE_TASKS: bool = True

    _assemble_accept_content = validator("CELERY_ACCEPT_CONTENT", allow_reuse=True)(assemble_value)


    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache(maxsize=128)
def get_settings():
    return Settings()


settings = get_settings()
