__all__ = ()
from enum import Enum

from fastapi import APIRouter, Request

from config.templates_config import templates


class Tags(Enum):
    homepage = 'Главная страница'


homepage_router = APIRouter()


@homepage_router.get('/homepage', tags=[Tags.homepage])
async def item_info(request: Request):
    return templates.TemplateResponse(
        request=request, name='todo/home.html',
    )
