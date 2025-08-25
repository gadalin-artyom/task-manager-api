import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

RUN_IN_DOCKER = os.getenv("IS_DOCKER", "not").lower() == "docker"

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class Settings(BaseSettings):
    app_name: str = Field("Task Manager API", alias="APP_NAME")
    app_env: str = Field("dev", alias="APP_ENV")
    app_debug: bool = Field(True, alias="APP_DEBUG")
    api_v1_prefix: str = Field("/api/v1", alias="API_V1_PREFIX")
    page_size_default: int = Field(20, alias="PAGE_SIZE_DEFAULT")

    postgres_db: str = Field("task_manager", alias="POSTGRES_DB")
    postgres_user: str = Field("postgres", alias="POSTGRES_USER")
    postgres_password: str = Field("postgres", alias="POSTGRES_PASSWORD")
    postgres_port: str = Field("5432", alias="POSTGRES_PORT")
    db_host: str = Field("localhost", alias="POSTGRES_HOST")

    log_path: str = "app/logs"

    model_config = SettingsConfigDict(
        env_file=(None if RUN_IN_DOCKER else ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        """Формирование строки подключения к базе данных."""
        print(f"DEBUG: RUN_IN_DOCKER = {RUN_IN_DOCKER}")
        print(f"DEBUG: IS_DOCKER env = {os.getenv('IS_DOCKER')}")

        if RUN_IN_DOCKER:
            host = "db"
            port = "5432"
        else:
            host = self.db_host
            port = self.postgres_port

        url = f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{host}:{port}/{self.postgres_db}"
        print(f"DEBUG: Database URL = {url}")
        return url


settings = Settings()
