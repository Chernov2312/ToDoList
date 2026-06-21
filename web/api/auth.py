__all__ = ()
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Cookie, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from config import Tags, settings, templates
from core.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from db.dao import UserDAO
from schemas.user import User

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


@auth_router.post('/register')
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
) -> Response:
    form_data = {'username': username, 'email': email, 'password': password}
    errors = {}
    try:
        _ = User(**form_data)
    except ValidationError as e:
        for error in e.errors():
            field = error['loc'][0]
            errors[field] = error['msg']
    if not errors:
        existing_user = await UserDAO.get_user(username)
        if existing_user is None:
            try:
                form_data['password'] = get_password_hash(
                    form_data['password'],
                )
                await UserDAO.add(form_data)
            except IntegrityError as e:
                error_msg = str(e).lower()
                if 'email' in error_msg and 'duplicate key' in error_msg:
                    errors['email'] = (
                        'Эта электронная почта уже зарегистрирована'
                    )
                elif 'username' in error_msg and 'duplicate key' in error_msg:
                    errors['username'] = 'Это имя пользователя уже занято'
                else:
                    errors['main'] = (
                        'Пользователь с такими данными уже существует'
                    )
        else:
            errors['username'] = 'Это имя пользователя уже занято'

    if errors:
        return templates.TemplateResponse(
            request=request,
            name='auth/register.html',
            context={
                'form_data': form_data,
                'errors': errors,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    response = RedirectResponse(
        url='/auth/login',
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key='registered',
        value='true',
        max_age=5,
    )
    return response


@auth_router.get('/login', response_class=HTMLResponse)
async def login_page(
    request: Request,
    registered: Optional[str] = Cookie(None, alias='registered'),
    flash_message: Optional[str] = Cookie(None, alias='flash_message'),
):
    registered = registered == 'true'
    response = templates.TemplateResponse(
        request=request,
        name='auth/login.html',
        context={
            'form_data': {},
            'errors': {},
            'registered': registered,
            'flash_message': flash_message,
        },
    )
    return response


@auth_router.post('/login')
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
) -> Response:
    user = await authenticate_user(username, password)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name='auth/login.html',
            context={
                'form_data': {'username': username},
                'errors': {'main': 'Неверное имя пользователя или пароль'},
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )

    response = RedirectResponse(
        url='/todo/v1/tasks',
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.set_cookie(
        key='access_token',
        value=f'Bearer {access_token}',
        httponly=True,
        samesite='lax',
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return response
