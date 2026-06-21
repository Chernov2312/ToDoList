__all__ = ()
from typing import Annotated

from fastapi import APIRouter, Depends, Request

from config import Tags, templates
from core.security import get_current_active_user
from schemas.user import UserProfile

user_router = APIRouter(tags=[Tags.user])


@user_router.get('/users/me/', description='Профиль')
async def get_profile(
    request: Request,
    current_user: Annotated[UserProfile, Depends(get_current_active_user)],
) -> UserProfile:
    return templates.TemplateResponse(
        request=request,
        name='user/profile',
        context=current_user.model_dump(),
    )
