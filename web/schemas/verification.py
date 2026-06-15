__all__ = ()
from typing import Optional

from pydantic import BaseModel, Field


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


class UserInDB(User):
    hashed_password: str = Field(
        ...,
        min_length=3,
        max_length=250,
        description='Пароль',
    )
