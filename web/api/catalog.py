__all__ = ()
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from config import Tags, templates
from core.security import get_current_active_user
from db.dao import TaskDAO
from schemas.item import Task
from schemas.user import User

catalog_router = APIRouter(tags=[Tags.catalog])


@catalog_router.get('/v1/task_info', response_class=HTMLResponse)
async def task_info(
    request,
    task: Task,
    _: User = Depends(get_current_active_user),
):
    context = {'Задание': task}
    return templates.TemplateResponse(
        request=request,
        name='todo/item_info.html',
        context=context,
    )


@catalog_router.get('/v1/tasks', response_class=HTMLResponse)
async def task_list(request, user: User = Depends(get_current_active_user)):
    context = {
        'Задания': user.tasks,
    }
    return templates.TemplateResponse(
        request=request,
        name='todo/task_list.html',
        context=context,
    )


@catalog_router.get('/v1/create_task', response_class=HTMLResponse)
async def create_task(
    request,
    task: Task,
    _: User = Depends(get_current_active_user),
):
    context = {'Задание': task}
    return templates.TemplateResponse(
        request=request,
        name='todo/create_task.html',
        context=context,
    )


@catalog_router.post('/v1/save_task', response_class=HTMLResponse)
async def save_task(
    request,
    task: Task,
    user: User = Depends(get_current_active_user),
):
    TaskDAO.add()
    return RedirectResponse('/catalog/v1/tasks')
