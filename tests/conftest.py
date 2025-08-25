import uuid
from unittest.mock import ANY, AsyncMock

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.api.v1 import tasks
from app.main import get_application


@pytest_asyncio.fixture
async def async_client():
    app = get_application()

    mock_service = AsyncMock()

    app.dependency_overrides[tasks.get_task_service] = lambda: mock_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client, mock_service


@pytest.mark.asyncio
async def test_create_task(async_client):
    client, mock_service = async_client

    task_id = str(uuid.uuid4())
    mock_service.create.return_value = {
        "id": task_id,
        "title": "Тестовая задача",
        "description": "Описание",
    }

    response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Тестовая задача", "description": "Описание"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Тестовая задача"
    assert data["description"] == "Описание"
    mock_service.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_task(async_client):
    client, mock_service = async_client

    task_id = str(uuid.uuid4())
    mock_service.get.return_value = {
        "id": task_id,
        "title": "Задача",
        "description": "Описание",
    }

    response = await client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Задача"
    assert data["description"] == "Описание"
    mock_service.get.assert_called_once_with(task_id)


@pytest.mark.asyncio
async def test_update_task(async_client):
    client, mock_service = async_client

    task_id = str(uuid.uuid4())
    mock_service.update.return_value = {
        "id": task_id,
        "title": "Обновлённая задача",
        "description": "Новое описание",
    }

    response = await client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Обновлённая задача", "description": "Новое описание"},
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Обновлённая задача"
    assert data["description"] == "Новое описание"
    mock_service.update.assert_called_once_with(task_id, ANY)


@pytest.mark.asyncio
async def test_delete_task(async_client):
    client, mock_service = async_client

    task_id = str(uuid.uuid4())
    mock_service.delete.return_value = True

    response = await client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_service.delete.assert_called_once_with(task_id)
