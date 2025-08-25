import uuid

from pydantic import BaseModel, Field, constr

from app.core.constants import TITLE_MAX_LENGTH, TITLE_MIN_LENGTH
from app.db.enums import TaskStatus

TitleStr = constr(min_length=TITLE_MIN_LENGTH, max_length=TITLE_MAX_LENGTH)


class TaskBase(BaseModel):
    title: TitleStr = Field(..., description="Название задачи")
    description: str | None = Field(None, description="Описание задачи")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: TitleStr | None = Field(None, description="Новое название задачи")
    description: str | None = Field(None, description="Новое описание задачи")
    status: TaskStatus | None = Field(None, description="Новый статус задачи")


class TaskOut(TaskBase):
    id: uuid.UUID
    status: TaskStatus

    model_config = {"from_attributes": True}
