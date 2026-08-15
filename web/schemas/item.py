__all__ = ()
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator, ConfigDict
from pydantic_core import PydanticCustomError


class Task(BaseModel):
    user_id: UUID
    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description='Название списка',
    )
    description: Optional[str] = Field(
        None,
        max_length=250,
        description='Описание',
    )
    deadline: Optional[datetime] = Field(
        None,
        description='Срок выполнения',
    )
    priority: Optional[str] = Field(
        'low',
        description='Приоритет выполнения',
    )

    @model_validator(mode='before')
    @classmethod
    def validate_and_clean_fields(cls, data: dict) -> dict:
        if 'description' in data and (data['description'] == '' or data['description'] is None):
            data['description'] = None

        deadline_val = data.get('deadline')

        if deadline_val == '' or deadline_val is None:
            data['deadline'] = None
            return data
        else:
            if isinstance(deadline_val, str):
                try:
                    if 'T' in deadline_val:
                        dt = datetime.strptime(deadline_val, '%Y-%m-%dT%H:%M')
                    else:
                        dt = datetime.strptime(deadline_val, '%Y-%m-%d')
                except ValueError:
                    raise PydanticCustomError('value_error', 'Неверный формат даты', {'loc': ('deadline',)})
            else:
                dt = deadline_val
            if dt and dt.date() < datetime.now().date():
                raise PydanticCustomError('value_error', 'Срок выполнения не может быть в прошлом', {'loc': ('deadline',)})

            data['deadline'] = dt
        return data


class TaskEdit(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description='Название списка',
    )
    description: Optional[str] = Field(
        None,
        max_length=250,
        description='Описание',
    )
    deadline: Optional[datetime] = Field(
        None,
        description='Срок выполнения',
    )
    priority: Optional[str] = Field(
        'low',
        description='Приоритет выполнения',
    )
    model_config = ConfigDict(from_attributes=True)


class Tasks(BaseModel):
    tasks: List[Task]
