import uuid
from unittest.mock import AsyncMock, patch

import anyio
import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from starlette import status

from app.db.db import get_async_session
from app.db.enums import TaskStatus
from app.main import get_application


@pytest.fixture
def client_and_service():
    """
    Клиент FastAPI (через ASGITransport) + мокнутый TaskService.
    Полностью без сети и без реальной БД.
    """
    app = get_application()

    async def override_get_db():
        yield AsyncMock(name="DummySession")

    app.dependency_overrides[get_async_session] = override_get_db

    service_mock = AsyncMock(name="TaskServiceMock")

    with patch("app.api.v1.tasks.TaskService", return_value=service_mock):
        transport = ASGITransport(app=app)
        client = AsyncClient(transport=transport, base_url="http://test")
        try:
            yield client, service_mock
        finally:
            anyio.run(client.aclose)


def _task_dict(
    *,
    id_: uuid.UUID | None = None,
    title: str = "Задача",
    description: str | None = "Описание",
    status: TaskStatus = TaskStatus.CREATED,
):
    return {
        "id": id_ or uuid.uuid4(),
        "title": title,
        "description": description,
        "status": status,
    }


@pytest.mark.asyncio
async def test_create_task(client_and_service):
    client, service = client_and_service

    payload = {"title": "Тестовая задача", "description": "Описание"}

    service.create.return_value = _task_dict(
        id_=uuid.uuid4(),
        title=payload["title"],
        description=payload["description"],
    )

    resp = await client.post("/api/v1/tasks/", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert uuid.UUID(data["id"])

    service.create.assert_called_once()


@pytest.mark.asyncio
async def test_get_task_ok(client_and_service):
    client, service = client_and_service

    tid = uuid.uuid4()
    service.get.return_value = _task_dict(
        id_=tid, title="Получить", description="Тест"
    )

    resp = await client.get(f"/api/v1/tasks/{tid}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["id"] == str(tid)
    assert data["title"] == "Получить"
    service.get.assert_called_once_with(tid)


@pytest.mark.asyncio
async def test_get_task_not_found(client_and_service):
    client, service = client_and_service

    tid = uuid.uuid4()
    service.get.return_value = None

    resp = await client.get(f"/api/v1/tasks/{tid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["detail"] == "Задача не найдена"
    service.get.assert_called_once_with(tid)


@pytest.mark.asyncio
async def test_list_tasks_ok(client_and_service):
    client, service = client_and_service

    t1 = _task_dict(title="Задача 1")
    t2 = _task_dict(title="Задача 2")
    service.list.return_value = [t1, t2]

    resp = await client.get("/api/v1/tasks/?page=1&page_size=10")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert [item["title"] for item in data["items"]] == [
        "Задача 1",
        "Задача 2",
    ]
    service.list.assert_called_once_with(page=1, page_size=10)


@pytest.mark.asyncio
async def test_update_task_ok(client_and_service):
    client, service = client_and_service

    tid = uuid.uuid4()
    service.update.return_value = _task_dict(
        id_=tid, title="Новая", description="Старое"
    )

    resp = await client.patch(f"/api/v1/tasks/{tid}", json={"title": "Новая"})
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["title"] == "Новая"
    assert data["id"] == str(tid)
    service.update.assert_called_once()


@pytest.mark.asyncio
async def test_update_task_not_found(client_and_service):
    client, service = client_and_service

    tid = uuid.uuid4()
    service.update.return_value = None

    resp = await client.patch(f"/api/v1/tasks/{tid}", json={"title": "Новая"})
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["detail"] == "Задача не найдена"
    service.update.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_ok(client_and_service):
    client, service = client_and_service

    tid = uuid.uuid4()
    service.delete.return_value = True

    resp = await client.delete(f"/api/v1/tasks/{tid}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    service.delete.assert_called_once_with(tid)


@pytest.mark.asyncio
async def test_delete_task_not_found(client_and_service):
    client, service = client_and_service

    tid = uuid.uuid4()
    service.delete.return_value = False

    resp = await client.delete(f"/api/v1/tasks/{tid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json()["detail"] == "Задача не найдена"
    service.delete.assert_called_once_with(tid)
