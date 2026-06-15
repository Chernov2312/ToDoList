__all__ = ()
from enum import Enum

from fastapi import APIRouter

from config.templates_config import templates


class Tags(Enum):
    items = 'Ассортимент'
    item = 'Инвормация о товаре'


catalog_router = APIRouter()


# @catalog_router.get('/v1/item_info', tags=[Tags.item])
# async def item_info(request):
#     context = {"id": id, "user_name": "Алексей"}
#     return templates.TemplateResponse(
#         request=request, name="item.html", context=context
#     )


# @catalog_router.get('/v1/catalog', tags=[Tags.items])
# async def item_list(request):
#     context = {"id": id, "user_name": "Алексей"}
#     return templates.TemplateResponse(
#         request=request, name="item.html", context=context
#     )
