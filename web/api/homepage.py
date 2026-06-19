__all__ = ()
from enum import Enum

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from config import Tags, templates

homepage_router = APIRouter(tags=Tags.homepage)


@homepage_router.get(
    '', description='Главная страница', response_class=HTMLResponse
)
async def item_info(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='todo/home.html',
    )
