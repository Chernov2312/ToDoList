__all__ = ()
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(25), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False)
    disabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
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
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    deadline: Mapped[datetime] = mapped_column(Date, nullable=True)
