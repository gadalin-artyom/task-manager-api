import uuid as uuid_pkg

from sqlalchemy import Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import TITLE_MAX_LENGTH
from app.db.db import Base
from app.db.enums import TaskStatus


class Task(Base):
    """Задача.
    Атрибуты:
    id: UUID первичный ключ
    title: название задачи (1..200 символов)
    description: произвольное текстовое описание
    status: статус задачи (created, in_progress, completed)
    """

    __tablename__ = "tasks"

    id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4
    )
    title: Mapped[str] = mapped_column(
        String(TITLE_MAX_LENGTH), nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.CREATED,
    )
