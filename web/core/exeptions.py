__all__ = ()
from urllib.parse import quote

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse


def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(401)
    async def custom_http_exception(
        request: Request, exc: HTTPException,
    ):
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            response = RedirectResponse(
                url='/auth/login',
                status_code=status.HTTP_303_SEE_OTHER,
            )

            encoded_message = quote(
                'Необходимо войти в аккаунт для просмотра этой страницы',
            )
            response.set_cookie(
                key='flash_message',
                value=encoded_message,
                max_age=5,
                httponly=True,
                samesite='lax',
            )
            return response

        return await request.app.default_exception_handler(request, exc)

    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            return RedirectResponse(
                url='/v1',
                status_code=status.HTTP_303_SEE_OTHER,
            )
        return await request.app.default_exception_handler(request, exc)
