from api.auth import auth_router
from api.catalog import catalog_router
from api.core import core_router
from api.homepage import homepage_router
from api.user import user_router

__all__ = (
    'auth_router',
    'catalog_router',
    'core_router',
    'homepage_router',
    'user_router',
)
