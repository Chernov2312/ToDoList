__all__ = ()
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import (
    auth_router,
    catalog_router,
    core_router,
    homepage_router,
    user_router,
)
from db.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    yield

    print('Остановка приложения и закрытие ресурсов...')


app = FastAPI(lifespan=lifespan, title='ToDoList', version='1.0.0')

app.include_router(prefix='', router=core_router)
app.include_router(prefix='', router=homepage_router)
app.include_router(prefix='/auth', router=auth_router)
app.include_router(prefix='/todo', router=catalog_router)
app.include_router(prefix='/user', router=user_router)

app.mount('/static', StaticFiles(directory='static_dev'), name='static')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
