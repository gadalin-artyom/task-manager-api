import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.db.enums import TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService


@pytest.mark.asyncio
async def test_service_create_commits_and_refreshes():
    db = AsyncMock()
    repo = AsyncMock()

    task = MagicMock()
    task.title = "t"
    task.description = "d"
    task.status = TaskStatus.CREATED

    repo.create.return_value = task

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        out = await svc.create(
            TaskCreate(title="t", description="d", status=TaskStatus.CREATED)
        )

    assert out.title == "t"
    assert out.description == "d"
    assert out.status == TaskStatus.CREATED
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_service_get_delegates_to_repo():
    db = AsyncMock()
    repo = AsyncMock()
    sentinel = object()
    repo.get.return_value = sentinel

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        got = await svc.get(uuid.uuid4())

    assert got is sentinel
    repo.get.assert_called_once()


@pytest.mark.asyncio
async def test_service_list_calculates_offset_and_limit():
    db = AsyncMock()
    repo = AsyncMock()
    repo.list.return_value = ["A", "B"]

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        items = await svc.list(page=3, page_size=5)

    assert items == ["A", "B"]
    repo.list.assert_called_once_with(offset=10, limit=5)


@pytest.mark.asyncio
async def test_service_update_found_changes_fields_and_commits():
    db = AsyncMock()
    repo = AsyncMock()

    class Obj:
        def __init__(self):
            self.title = "old"
            self.description = "old"
            self.status = TaskStatus.CREATED

    obj = Obj()
    repo.get.return_value = obj
    repo.update.return_value = obj

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        out = await svc.update(
            uuid.uuid4(),
            TaskUpdate(
                title="new", description=None, status=TaskStatus.COMPLETED
            ),
        )

    assert out.title == "new"
    assert out.description == "old"
    assert out.status == TaskStatus.COMPLETED
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()
    repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_service_update_all_fields():
    db = AsyncMock()
    repo = AsyncMock()

    class Obj:
        def __init__(self):
            self.title = "old"
            self.description = "old"
            self.status = TaskStatus.CREATED

    obj = Obj()
    repo.get.return_value = obj
    repo.update.return_value = obj

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        out = await svc.update(
            uuid.uuid4(),
            TaskUpdate(
                title="new",
                description="new desc",
                status=TaskStatus.COMPLETED,
            ),
        )

    assert out.title == "new"
    assert out.description == "new desc"
    assert out.status == TaskStatus.COMPLETED
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()
    repo.update.assert_called_once()


@pytest.mark.asyncio
async def test_service_update_not_found_returns_none():
    db = AsyncMock()
    repo = AsyncMock()
    repo.get.return_value = None

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        out = await svc.update(uuid.uuid4(), TaskUpdate(title="x"))

    assert out is None
    db.commit.assert_not_called()
    db.refresh.assert_not_called()


@pytest.mark.asyncio
async def test_service_delete_found_commit_and_true():
    db = AsyncMock()
    repo = AsyncMock()

    task = MagicMock()
    repo.get.return_value = task
    repo.delete.return_value = None

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        ok = await svc.delete(uuid.uuid4())

    assert ok is True
    repo.delete.assert_called_once()
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_service_delete_not_found_returns_false():
    db = AsyncMock()
    repo = AsyncMock()
    repo.get.return_value = None

    with patch("app.services.task_service.TaskRepository", return_value=repo):
        svc = TaskService(db)
        ok = await svc.delete(uuid.uuid4())

    assert ok is False
    repo.delete.assert_not_called()
    db.commit.assert_not_called()
