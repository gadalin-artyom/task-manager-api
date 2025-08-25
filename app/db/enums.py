from enum import Enum


class TaskStatus(str, Enum):
    CREATED = "Создано"
    IN_PROGRESS = "В работе"
    COMPLETED = "Завершено"
