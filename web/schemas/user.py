__all__ = ()
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=25,
        description='Имя пользователя',
    )
    email: Optional[str] = Field(
        None,
        min_length=3,
        max_length=250,
        description='Почта',
    )
    tasks: List[dict] = Field(..., description='Список заданий')
    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=25,
        description='Имя пользователя',
    )
    email: Optional[str] = Field(
        None,
        min_length=3,
        max_length=250,
        description='Почта',
    )
    tasks: List[dict] = Field(..., description='Список заданий')
