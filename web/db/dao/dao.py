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
        query = select(User).filter_by(username=target_username)
        result = await session.execute(query)
        return result.scalar_one_or_none()


class TaskDAO(BaseDAO):
    model = Task
