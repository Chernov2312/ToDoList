__all__ = ()
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(25), nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False)
    tasks: Mapped[list['Task']] = relationship(
        'Task',
        back_populates='user',
        cascade='all, delete-orphan',
    )


class Task(Base):
    user: Mapped['User'] = relationship(
        'User',
        back_populates='tasks',
    )
    description: Mapped[str] = mapped_column(String(500), nullable=False)
