__all__ = ()
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from config import settings
from db.dao import UserDAO
from schemas.user import User
from schemas.verification import TokenData, UserAuth

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash('dummypassword')


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get('Authorization')
        if authorization:
            scheme, param = (
                authorization.split(' ')
                if ' ' in authorization
                else (None, None)
            )
            if scheme and scheme.lower() == 'bearer':
                return param

        token_cookie = request.cookies.get('access_token')
        if token_cookie:
            if token_cookie.startswith('Bearer '):
                return token_cookie.split(' ')[1]
            return token_cookie
        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authenticated',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return None


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl='core/token',
    auto_error=True,
)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


async def authenticate_user(username: str, password: str):
    user = await UserDAO.get_user(username)
    if user is None:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False
    return UserAuth.model_validate(user)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user_db = await UserDAO.get_user(username=token_data.username)
    user = User.model_validate(user_db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Неактивный пользователь')
    return current_user
