import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    CORE_DB_DRIVER: str = os.getenv("CORE_DB_DRIVER", "sqlite")
    CORE_DB_HOST: str = os.getenv("CORE_DB_HOST", "")
    CORE_DB_PORT: str = os.getenv("CORE_DB_PORT", "")
    CORE_DB_USER: str = os.getenv("CORE_DB_USER", "")
    CORE_DB_PASSWORD: str = os.getenv("CORE_DB_PASSWORD", "")
    CORE_DB_NAME: str = os.getenv("CORE_DB_NAME", "core.db")

    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key-change-in-production")

    TENANT_DB_TEMPLATE: str = os.getenv(
        "TENANT_DB_TEMPLATE", "{driver}://{host}{port}{user}{password}{db_name}"
    )

    TENANT_DB_DRIVER: str = os.getenv("TENANT_DB_DRIVER", "sqlite")
    TENANT_DB_HOST: str = os.getenv("TENANT_DB_HOST", "")
    TENANT_DB_PORT: str = os.getenv("TENANT_DB_PORT", "")
    TENANT_DB_USER: str = os.getenv("TENANT_DB_USER", "")
    TENANT_DB_PASSWORD: str = os.getenv("TENANT_DB_PASSWORD", "")

    @property
    def core_db_url(self) -> str:
        """Formats the URL for connecting to the main DB."""
        if self.CORE_DB_DRIVER == "sqlite":
            return f"sqlite://{self.CORE_DB_NAME}"

        port = f":{self.CORE_DB_PORT}" if self.CORE_DB_PORT else ""
        user = (
            f"{self.CORE_DB_USER}:{self.CORE_DB_PASSWORD}@" if self.CORE_DB_USER else ""
        )

        db_url = (
            f"{self.CORE_DB_DRIVER}://"
            f"{user}{self.CORE_DB_HOST}{port}/{self.CORE_DB_NAME}"
        )
        return db_url


@lru_cache()
def get_settings() -> Settings:
    return Settings()
