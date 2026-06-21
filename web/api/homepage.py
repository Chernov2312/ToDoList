__all__ = ()
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from config import Tags, templates

homepage_router = APIRouter(tags=[Tags.homepage])


@homepage_router.get(
    '/v1',
    description='Главная страница',
    response_class=HTMLResponse,
)
async def homepage(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='homepage/home.html',
    )
