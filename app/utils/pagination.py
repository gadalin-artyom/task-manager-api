from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.core.constants import MIN_PAGE_SIZE

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    page: int = Field(MIN_PAGE_SIZE, ge=MIN_PAGE_SIZE)
    page_size: int = Field(MIN_PAGE_SIZE, ge=MIN_PAGE_SIZE)
