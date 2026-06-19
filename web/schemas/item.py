__all__ = ()
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: UUID
    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description='Название списка',
    )
    descripton: Optional[str] = Field(
        None,
        min_length=3,
        max_length=250,
        description='Описание',
    )
