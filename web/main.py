__all__ = ()
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

app = FastAPI()

app.include_router(prefix='', router=core_router)
app.include_router(prefix='', router=homepage_router)
app.include_router(prefix='/auth', router=auth_router)
app.include_router(prefix='/todo', router=catalog_router)
app.include_router(prefix='/user', router=user_router)

app.mount('/static', StaticFiles(directory='static_dev'), name='static')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
