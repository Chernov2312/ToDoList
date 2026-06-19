__all__ = ()
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from config import Tags, settings, templates
from core.security import authenticate_user, create_access_token
from db.dao import UserDAO
from schemas.verification import Token, User

auth = APIRouter(tags=Tags.auth)


@auth.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='auth/register.html',
        context={
            'form_data': {},
            'errors': {},
        },
    )


@auth.post('/register', response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    form_data = {'username': username, 'email': email, 'password': password}
    errors = {}
    try:
        _ = User(**form_data)
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


@auth.get('/login', response_class=HTMLResponse)
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


@auth.post('/login')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(
        form_data.username,
        form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer')
