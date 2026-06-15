__all__ = ()
from typing import List, Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
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
    tasks: List[dict] = Field(..., description='Список заданий')
