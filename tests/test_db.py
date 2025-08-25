import os
from unittest.mock import patch

from app.core.config import Settings


def test_database_url_local_debug(capsys):
    with patch.dict(
        os.environ,
        {
            "IS_DOCKER": "false",
            "POSTGRES_HOST": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_pass",
            "POSTGRES_DB": "test_db",
        },
    ):
        with patch("app.core.config.RUN_IN_DOCKER", False):
            settings = Settings()
            url = settings.database_url

            captured = capsys.readouterr()
            assert "DEBUG: RUN_IN_DOCKER = False" in captured.out
            assert "DEBUG: IS_DOCKER env = false" in captured.out
            assert (
                "DEBUG: Database URL = postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db"
                in captured.out
            )
            assert (
                url
                == "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db"
            )


def test_database_url_docker_debug(capsys):
    with patch.dict(
        os.environ,
        {
            "IS_DOCKER": "true",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_pass",
            "POSTGRES_DB": "test_db",
        },
    ):
        with patch("app.core.config.RUN_IN_DOCKER", True):
            settings = Settings()
            url = settings.database_url

            captured = capsys.readouterr()
            assert "DEBUG: RUN_IN_DOCKER = True" in captured.out
            assert "DEBUG: IS_DOCKER env = true" in captured.out
            assert (
                "DEBUG: Database URL = postgresql+asyncpg://test_user:test_pass@db:5432/test_db"
                in captured.out
            )
            assert (
                url
                == "postgresql+asyncpg://test_user:test_pass@db:5432/test_db"
            )


def test_database_url_docker_lowercase(capsys):
    with patch.dict(
        os.environ,
        {
            "IS_DOCKER": "docker",
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_pass",
            "POSTGRES_DB": "test_db",
        },
    ):
        with patch("app.core.config.RUN_IN_DOCKER", True):
            settings = Settings()
            _ = settings.database_url

            captured = capsys.readouterr()
            assert "DEBUG: RUN_IN_DOCKER = True" in captured.out
            assert "DEBUG: IS_DOCKER env = docker" in captured.out


def test_database_url_default_values():
    with patch.dict(os.environ, {}, clear=True):
        with patch("app.core.config.RUN_IN_DOCKER", False):
            settings = Settings()
            url = settings.database_url
            assert (
                "postgresql+asyncpg://postgres:postgres@localhost:5432/task_manager"
                in url
            )
