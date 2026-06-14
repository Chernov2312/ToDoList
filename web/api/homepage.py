from fastapi import APIRouter
from enum import Enum

from main import templates


class Tags(Enum):
    users = "users"
    items = "items"
    item = 'item'


homepage_router = APIRouter()


@homepage_router.get('/v1/item_info', tags=[Tags.item])
async def item_info(request):
    context = {
        "id": id,
        "user_name": "Алексей"
    }
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context=context
    )

@homepage_router.get()
async def item_list(request):
    context = {
        "id": id,
        "user_name": "Алексей"
    }
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context=context
    )