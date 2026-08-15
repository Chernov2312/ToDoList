__all__ = ()
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.dao.base import BaseDAO
from db.database import connection
from db.models import Task, User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    @connection
    async def get_user(cls, username: str, *, session: AsyncSession):
        query = select(User).filter_by(username=username)
        result = await session.execute(query)
        return result.scalar_one_or_none()


class TaskDAO(BaseDAO):
    model = Task

    @classmethod
    @connection
    async def get_all_tasks(cls, user_id: UUID, *, session: AsyncSession):
        query = select(Task).filter_by(user_id=user_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @connection
    async def toggle_complete(cls, task_id: UUID, *, session: AsyncSession):
        stmt = (
            update(cls.model)
            .where(cls.model.id == task_id)
            .values(is_complete=~cls.model.is_complete)
        )
        await session.execute(stmt)
        await session.commit()
