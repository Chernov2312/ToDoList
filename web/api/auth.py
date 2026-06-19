__all__ = ()
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from config import Tags, templates
from core.security import authenticate_user
from db.dao import UserDAO
from schemas.verification import UserAuth

auth_router = APIRouter(tags=[Tags.auth])


@auth_router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='auth/register.html',
        context={
            'form_data': {},
            'errors': {},
        },
    )


@auth_router.post('/register', response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    form_data = {'username': username, 'email': email, 'password': password}
    errors = {}
    try:
        _ = UserAuth(**form_data)
    except ValidationError as e:
        for error in e.errors():
            field = error['loc'][0]
            errors[field] = error['msg']

    if not errors:
        existing_user = UserDAO.get_user(username)
        if existing_user:
            try:
                await UserDAO.add(form_data)
            except IntegrityError as e:
                if email in str(e):
                    errors['email'] = 'Почта занята'
                elif username in str(e):
                    errors['username'] = (
                        'Пользователь с таким именем уже существует'
                    )

    if errors:
        return templates.TemplateResponse(
            request=request,
            name='register.html',
            context={
                'form_data': form_data,
                'errors': errors,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return RedirectResponse(
        url='/auth/login',
        status_code=status.HTTP_303_SEE_OTHER,
        registered=True,
    )


@auth_router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request, registered: bool):
    return templates.TemplateResponse(
        request=request,
        name='auth/register.html',
        context={
            'form_data': {},
            'errors': {},
            'registered': registered,
        },
    )


@auth_router.post('/login', response_class=HTMLResponse)
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if authenticate_user(username=username, password=password):
        return templates.TemplateResponse(
            request=request,
            name='auth/todo.html',
            context={},
        )
    return templates.TemplateResponse(
        request=request,
        name='auth/register.html',
        context={
            'form_data': {},
            'errors': {},
        },
    )
