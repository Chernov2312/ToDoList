from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from api.homepage import homepage_router

app = FastAPI()
app.include_router(prefix='/', router=homepage_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

if __name__ == '__main__':
    uvicorn.run(app)
