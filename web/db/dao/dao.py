__all__ = ()
from dao.base import BaseDAO
from database import connection
from models import Task, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAO(BaseDAO):
    model = User

    @connection
    async def get_user(target_username: str, session: AsyncSession):
        user: User = select(User).filter_by(username=target_username)
        return user


class TaskDAO(BaseDAO):
    model = Task
