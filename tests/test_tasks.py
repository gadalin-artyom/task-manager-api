import uuid
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from starlette import status

from app.db.enums import TaskStatus
from app.main import app
from app.schemas.task import TaskOut


@pytest.mark.asyncio
async def test_create_task():
    mock_task = TaskOut(
        id=uuid.uuid4(),
        title="Тест №1",
        description="Описание",
        status=TaskStatus.CREATED,
    )

    with patch(
        "app.services.task_service.TaskService.create", return_value=mock_task
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/api/v1/tasks/",
                json={
                    "title": "TТест №1",
                    "description": "Описание",
                    "status": "Создано",
                },
            )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == mock_task.title
    assert data["description"] == mock_task.description
    assert data["status"] == mock_task.status


@pytest.mark.asyncio
async def test_get_task():
    task_id = uuid.uuid4()
    mock_task = TaskOut(
        id=task_id,
        title="Тест №1",
        description="Описание",
        status=TaskStatus.CREATED,
    )

    with patch(
        "app.services.task_service.TaskService.get", return_value=mock_task
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(mock_task.id)
    assert data["title"] == mock_task.title
    assert data["description"] == mock_task.description
    assert data["status"] == mock_task.status


@pytest.mark.asyncio
async def test_get_task_not_found():
    with patch("app.services.task_service.TaskService.get", return_value=None):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/api/v1/tasks/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Задача не найдена"


@pytest.mark.asyncio
async def test_list_tasks():
    mock_task = TaskOut(
        id=uuid.uuid4(),
        title="Task 1",
        description="desc",
        status=TaskStatus.CREATED,
    )
    mock_page = [mock_task]

    with patch(
        "app.services.task_service.TaskService.list", return_value=mock_page
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/v1/tasks/?page=1&page_size=10")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == str(mock_task.id)
    assert data["items"][0]["title"] == mock_task.title
    assert data["items"][0]["description"] == mock_task.description
    assert data["items"][0]["status"] == mock_task.status


@pytest.mark.asyncio
async def test_update_task():
    task_id = uuid.uuid4()
    updated_task = TaskOut(
        id=task_id,
        title="Updated",
        description="new",
        status=TaskStatus.IN_PROGRESS,
    )

    with patch(
        "app.services.task_service.TaskService.update",
        return_value=updated_task,
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.patch(
                f"/api/v1/tasks/{task_id}",
                json={
                    "title": "Updated",
                    "description": "new",
                    "status": TaskStatus.IN_PROGRESS,
                },
            )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(updated_task.id)
    assert data["title"] == updated_task.title
    assert data["description"] == updated_task.description
    assert data["status"] == updated_task.status


@pytest.mark.asyncio
async def test_update_task_not_found():
    with patch(
        "app.services.task_service.TaskService.update", return_value=None
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.patch(
                f"/api/v1/tasks/{uuid.uuid4()}", json={"title": "X"}
            )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Задача не найдена"


@pytest.mark.asyncio
async def test_delete_task():
    task_id = uuid.uuid4()

    with patch(
        "app.services.task_service.TaskService.delete", return_value=True
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_task_not_found():
    with patch(
        "app.services.task_service.TaskService.delete", return_value=False
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.delete(f"/api/v1/tasks/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Задача не найдена"
