__all__ = ()
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str | None] = Field(
        None,
        min_length=3,
        max_length=25,
        description='Имя пользователя',
    )


class UserAuth(BaseModel):
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
    model_config = ConfigDict(from_attributes=True)
