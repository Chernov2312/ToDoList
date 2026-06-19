__all__ = ()
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from config import Tags, templates
from core.security import get_current_active_user
from schemas.item import Task
from schemas.user import User

catalog_router = APIRouter(tags=[Tags.catalog])


@catalog_router.get('/v1/task_info', response_class=HTMLResponse)
async def item_info(
    request,
    task: Task,
    _: User = Depends(get_current_active_user),
):
    context = {'Задание': task}
    return templates.TemplateResponse(
        request=request,
        name='item.html',
        context=context,
    )


@catalog_router.get('/v1/tasks', response_class=HTMLResponse)
async def item_list(request, user: User = Depends(get_current_active_user)):
    context = {
        'Задания': user.tasks,
    }
    return templates.TemplateResponse(
        request=request,
        name='items.html',
        context=context,
    )
