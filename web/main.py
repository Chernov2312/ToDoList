__all__ = ()
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.homepage import homepage_router

app = FastAPI()
app.include_router(prefix='/v1', router=homepage_router)

app.mount('/static', StaticFiles(directory='static_dev'), name='static')

if __name__ == '__main__':
    uvicorn.run(app)
