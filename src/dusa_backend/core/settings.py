import os
from enum import StrEnum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvEnum(StrEnum):
    TESTING = "TESTING"
    LOCAL = "LOCAL"
    DEV = "DEV"
    STG = "STG"
    PRD = "PRD"


ENV = EnvEnum(os.environ["ENV"]) if "ENV" in os.environ else EnvEnum.TESTING
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE_MAPPING = {
    EnvEnum.TESTING: BACKEND_DIR / ".env.testing",
    EnvEnum.LOCAL: BACKEND_DIR / ".env.local-dev",
}


class Settings(BaseSettings):
    """
    API and env settings set here to be accesses across the API.
    """

    # general
    env: EnvEnum = EnvEnum.TESTING

    # postgres settings
    db_user: str | None = None
    db_password: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_name: str | None = None

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_MAPPING.get(ENV),  # loads a .env file for testing or local use only
        extra="ignore",
        json_schema_extra={
            "fields": {
                # general
                "env": {"env": "ENV"},
                # postgres
                "db_user": {"env": "DB_USER"},
                "db_password": {"env": "DB_PASSWORD"},
                "db_host": {"env": "DB_HOST"},
                "db_port": {"env": "DB_PORT"},
                "db_name": {"env": "DB_NAME"},
            },
        },
    )

    @property
    def db_uri(self) -> str:
        """
        Builds the database URI from the environment variables provided.
        """
        pwd = f":{self.db_password}" if self.db_password else ""
        return f"postgresql://{self.db_user}{pwd}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
