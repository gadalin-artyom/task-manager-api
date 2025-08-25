import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.task_repository import TaskRepository


@pytest.mark.asyncio
async def test_create_calls_db_methods():
    db = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(db)
    task = Task(title="Test", description="Desc", status="created")

    out = await repo.create(task)

    db.add.assert_called_once_with(task)
    db.flush.assert_called_once()
    db.refresh.assert_called_once_with(task)
    assert out is task


@pytest.mark.asyncio
async def test_get_returns_task():
    db = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(db)
    task_id = uuid.uuid4()

    db.get.return_value = "task"
    out = await repo.get(task_id)

    db.get.assert_called_once_with(Task, task_id)
    assert out == "task"


@pytest.mark.asyncio
async def test_list_executes_select_and_returns_tasks():
    db = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(db)

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = ["task1", "task2"]

    db.execute.return_value = mock_result

    out = await repo.list(offset=5, limit=10)
    db.execute.assert_called_once()
    assert out == ["task1", "task2"]


@pytest.mark.asyncio
async def test_update_calls_db_methods():
    db = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(db)
    task = Task(title="Old", description="Old", status="created")
    out = await repo.update(task)

    db.add.assert_called_once_with(task)
    db.flush.assert_called_once()
    db.refresh.assert_called_once_with(task)
    assert out is task


@pytest.mark.asyncio
async def test_delete_calls_db_delete():
    db = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(db)
    task = Task(title="Old", description="Old", status="created")
    await repo.delete(task)
    db.delete.assert_called_once_with(task)
