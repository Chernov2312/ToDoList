__all__ = ()
import uuid
from typing import Any, Dict, List

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
    async def get_by_id(cls, session: AsyncSession, id: uuid.UUID):
        item = session.get(cls.model, id)
        return item
