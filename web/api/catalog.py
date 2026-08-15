__all__ = ()
from datetime import datetime
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from config import Tags, templates
from core.security import get_current_active_user
from db.dao import TaskDAO
from schemas.item import Task, TaskEdit
from schemas.user import User
from schemas.verification import UserAuth

catalog_router = APIRouter(tags=[Tags.catalog])


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
        name='/todo/task_list.html',
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
    priority: str = Form(...),
    user: UserAuth = Depends(get_current_active_user),
) -> Response:
    form_data = {
        'title': title,
        'description': description,
        'deadline': deadline,
        'priority': priority,
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
            name='/todo/create_task.html',
            context={
                'form_data': form_data,
                'errors': errors,
                'user': user,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    await TaskDAO.add(Task(**form_data).model_dump(mode='python'))
    response = RedirectResponse(
        url='/todo/v1/create_task',
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key='created_task',
        value='true',
        max_age=5,
    )
    return response


@catalog_router.post('/v1/complete', name='toggle_task')
async def toggle_task(
    task_id: UUID = Form(...),
    _: UserAuth = Depends(get_current_active_user),
) -> RedirectResponse:
    await TaskDAO.toggle_complete(task_id)
    response = RedirectResponse(
        url='/todo/v1/tasks',
        status_code=status.HTTP_303_SEE_OTHER,
    )
    res = await TaskDAO.get_by_id(task_id)
    print(res.is_complete)
    return response


@catalog_router.get('/v1/task_info/{task_id}', response_class=HTMLResponse)
async def task_info(
    request: Request,
    task_id: UUID,
    user: UserAuth = Depends(get_current_active_user),
):
    return templates.TemplateResponse(
        request=request,
        name='/todo/task_info.html',
        context={
            'task': await TaskDAO.get_by_id(task_id),
            'user': user,
        },
    )


@catalog_router.post('/v1/edit/{task_id}', name='edit_task')
async def edit_task(
    task_id: UUID,
    title: str = Form(...),
    description: str = Form(None),
    deadline: datetime = Form(...),
    priority: str = Form(...),
    _: UserAuth = Depends(get_current_active_user),
) -> RedirectResponse:
    task = TaskEdit(
        **{
            'title': title,
            'description': description,
            'deadline': deadline,
            'priority': priority,
        },
    )
    await TaskDAO.edit(task_id, task.model_dump(mode='python'))
    return RedirectResponse(url='/todo/v1/tasks', status_code=status.HTTP_303_SEE_OTHER)


@catalog_router.post('/v1/delete_task/{task_id}', name='delete_task')
async def delete_task(
    task_id: UUID,
    _: UserAuth = Depends(get_current_active_user),
) -> RedirectResponse:
    await TaskDAO.delete_by_id(task_id)
    response = RedirectResponse(
        url='/todo/v1/tasks',
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key='delete_task',
        value='true',
        max_age=5,
    )
    return response
