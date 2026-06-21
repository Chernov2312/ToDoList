__all__ = ()
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dao.base import BaseDAO
from db.database import connection
from db.models import Task, User


class UserDAO(BaseDAO):
    model = User

    @connection
    async def get_user(username: str, session: AsyncSession):
        query = select(User).filter_by(username=username)
        result = await session.execute(query)
        return result.scalar_one_or_none()


class TaskDAO(BaseDAO):
    model = Task

    @connection
    async def get_all_tasks(user_id: UUID, session: AsyncSession):
        querry = select(Task).filter_by(user_id=user_id)
        result = await session.execute(querry)
        return result.scalars().all()
