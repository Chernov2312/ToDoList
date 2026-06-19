__all__ = ()
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Depends, Request

from config import Tags, templates
from core.security import get_current_active_user
from schemas.verification import User

user_router = APIRouter(tags=Tags.user)


@user_router.get('/users/me/', description='Профиль')
async def get_profile(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return templates.TemplateResponse(
        request=request,
        name='todo/profile',
        context=current_user.model_dump(),
    )
