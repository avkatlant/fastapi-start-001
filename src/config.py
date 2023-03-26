# import os
from functools import lru_cache
from typing import Any, cast

# from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, validator

# load_dotenv()

# DB_HOST: Final[str] = os.environ.get("DB_HOST", "")
# DB_PORT: Final[str] = os.environ.get("DB_PORT", "")
# DB_NAME: Final[str] = os.environ.get("DB_NAME", "")
# DB_USER: Final[str] = os.environ.get("DB_USER", "")
# DB_PASS: Final[str] = os.environ.get("DB_PASS", "")

# SECRET_AUTH: Final[str] = os.environ.get("SECRET_AUTH", "")


class AppSettings(BaseSettings):
    ENV_NAME: str

    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    SQL_SHOW_QUERY: bool

    DATABASE_URL: str = ""

    SECRET_AUTH: str

    @validator("DATABASE_URL", pre=True)
    def get_database_url(cls, v: str | None, values: dict[str, Any]) -> str:
        if isinstance(v, str) and v:
            return v
        result = cast(
            str,
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values.get("DB_USER"),
                password=values.get("DB_PASS"),
                host=values.get("DB_HOST"),
                port=values.get("DB_PORT"),
                path=f"/{values.get('DB_NAME')}",
            ),
        )
        return result

    class Config:
        env_file = ".env", ".env_dev"
        env_file_encoding = "utf-8"


@lru_cache
def get_app_settings() -> AppSettings:
    settings = AppSettings()  # type: ignore
    print(f">>> Loading settings for: {settings.ENV_NAME}")
    return settings
