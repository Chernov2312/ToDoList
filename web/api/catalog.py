__all__ = ()
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from config import Tags, templates
from core.security import get_current_active_user
from db.dao import TaskDAO
from schemas.item import Task
from schemas.user import User
from schemas.verification import UserAuth

catalog_router = APIRouter(tags=[Tags.catalog])


@catalog_router.get('/v1/task_info', response_class=HTMLResponse)
async def task_info(
    request: Request,
    task: Task,
    user: UserAuth = Depends(get_current_active_user),
):
    context = {'Задание': task, 'user': user}
    return templates.TemplateResponse(
        request=request,
        name='todo/item_info.html',
        context=context,
    )


@catalog_router.get('/v1/tasks', response_class=HTMLResponse)
async def task_list(
    request: Request,
    delete: Optional[str] = Cookie(None, alias='created_task'),
    user: User = Depends(get_current_active_user),
):
    tasks = await TaskDAO.get_all_tasks(user.id)

    context = {
        'tasks': tasks,
        'delete': delete == 'true',
        'user': user,
    }
    return templates.TemplateResponse(
        request=request,
        name='todo/task_list.html',
        context=context,
    )


@catalog_router.get('/v1/create_task', response_class=HTMLResponse)
async def create_task_page(
    request: Request,
    created: Optional[str] = Cookie(None, alias='created_task'),
    user: UserAuth = Depends(get_current_active_user),
):
    return templates.TemplateResponse(
        request=request,
        name='todo/create_task.html',
        context={
            'form_data': {},
            'errors': {},
            'created': created == 'true',
            'user': user,
        },
    )


@catalog_router.post('/v1/create_task')
async def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    deadline: str = Form(...),
    user: UserAuth = Depends(get_current_active_user),
) -> Response:
    form_data = {
        'title': title,
        'description': description,
        'deadline': deadline,
        'user_id': user.id,
    }
    errors = {}
    try:
        _ = Task(**form_data)
    except ValidationError as e:
        for error in e.errors():
            field = error['loc'][0]
            errors[field] = error['msg']
    if errors:
        return templates.TemplateResponse(
            request=request,
            name='todo/create_task.html',
            context={
                'form_data': form_data,
                'errors': errors,
                'user': user,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    await TaskDAO.add(form_data)
    response = RedirectResponse(
        url='todo/v1/create_task',
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key='created_task',
        value='true',
        max_age=5,
    )
    return response


@catalog_router.post('/v1/delete')
async def delete_task(
    task_id: str = Form(...),
    _: UserAuth = Depends(get_current_active_user),
) -> RedirectResponse:
    await TaskDAO.delete(task_id)
    response = RedirectResponse(
        url='todo/v1/tasks',
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key='delete_task',
        value='true',
        max_age=5,
    )
    return response
