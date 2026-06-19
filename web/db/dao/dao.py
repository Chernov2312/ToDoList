__all__ = ()
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dao.base import BaseDAO
from db.database import connection
from db.models import Task, User


class UserDAO(BaseDAO):
    model = User

    @connection
    async def get_user(target_username: str, session: AsyncSession):
        user: User = select(User).filter_by(username=target_username)
        return user


class TaskDAO(BaseDAO):
    model = Task
