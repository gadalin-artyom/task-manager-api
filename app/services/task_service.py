import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import DEFAULT_PAGE_SIZE
from app.db.enums import TaskStatus
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Асинхронный сервис-обёртка над репозиторием с бизнес-правилами."""

    def __init__(self, db: AsyncSession):
        self.repo = TaskRepository(db)
        self.db = db

    async def create(self, data: TaskCreate) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            status=TaskStatus.CREATED,
        )
        task = await self.repo.create(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get(self, task_id: uuid.UUID) -> Task | None:
        return await self.repo.get(task_id)

    async def list(
        self, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE
    ) -> list[Task]:
        offset = max(page - 1, 0) * page_size
        return await self.repo.list(offset=offset, limit=page_size)

    async def update(
        self, task_id: uuid.UUID, data: TaskUpdate
    ) -> Task | None:
        task = await self.repo.get(task_id)
        if not task:
            return None
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status
        task = await self.repo.update(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task_id: uuid.UUID) -> bool:
        task = await self.repo.get(task_id)
        if not task:
            return False
        await self.repo.delete(task)
        await self.db.commit()
        return True
