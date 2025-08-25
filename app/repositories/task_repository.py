import uuid
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_PAGE_SIZE
from app.models.task import Task


class TaskRepository:
    """Асинхронный репозиторий для операций с задачами."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj: Task) -> Task:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def get(self, task_id: uuid.UUID) -> Task | None:
        return await self.db.get(Task, task_id)

    async def list(
        self, offset: int = 0, limit: int = DEFAULT_PAGE_SIZE
    ) -> List[Task]:
        stmt = select(Task).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, obj: Task) -> Task:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: Task) -> None:
        await self.db.delete(obj)
        await self.db.flush()
