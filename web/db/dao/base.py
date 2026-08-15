__all__ = ()
import uuid
from typing import Any, Dict, List

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import connection


class BaseDAO:
    model = None

    @classmethod
    @connection
    async def add(cls, values, *, session: AsyncSession):
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    @connection
    async def add_many(
        cls,
        instances: List[Dict[str, Any]],
        session: AsyncSession,
    ):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    @classmethod
    @connection
    async def get_by_id(cls, cur_id: uuid.UUID, *, session: AsyncSession):
        query = select(cls.model).filter_by(id=cur_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @connection
    async def delete_by_id(cls, cur_id: uuid.UUID, *, session: AsyncSession):
        query = delete(cls.model).filter_by(id=cur_id)
        result = await session.execute(query)
        return result.rowcount

    @classmethod
    @connection
    async def edit(cls, cur_id: uuid.UUID, data: dict, *, session: AsyncSession):
        stmt = update(cls.model).where(cls.model.id == cur_id).values(**data)
        result = await session.execute(stmt)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount > 0
