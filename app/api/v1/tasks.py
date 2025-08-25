import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_PAGE_SIZE
from app.db.db import get_async_session
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import TaskService
from app.utils.pagination import Page

router = APIRouter()


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate, db: AsyncSession = Depends(get_async_session)
):
    """Создать задачу."""
    task_service = TaskService(db)
    task = await task_service.create(payload)
    return TaskOut.model_validate(task)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: uuid.UUID, db: AsyncSession = Depends(get_async_session)
):
    """Получить задачу по UUID."""
    task_service = TaskService(db)
    task = await task_service.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return TaskOut.model_validate(task)


@router.get("/", response_model=Page[TaskOut])
async def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=200),
    db: AsyncSession = Depends(get_async_session),
):
    """Список задач с пагинацией."""
    task_service = TaskService(db)
    tasks = await task_service.list(page=page, page_size=page_size)
    return Page[TaskOut](
        items=[TaskOut.model_validate(t) for t in tasks],
        page=page,
        page_size=page_size,
    )


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: uuid.UUID,
    payload: TaskUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """Частично обновить задачу."""
    task_service = TaskService(db)
    task = await task_service.update(task_id, payload)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return TaskOut.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID, db: AsyncSession = Depends(get_async_session)
):
    """Удалить задачу."""
    task_service = TaskService(db)
    ok = await task_service.delete(task_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return None
