__all__ = ()
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class Task(BaseModel):
    id: UUID
    user_id: UUID
    title: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description='Название списка',
    )
    description: Optional[str] = Field(
        None,
        min_length=3,
        max_length=250,
        description='Описание',
    )
    deadline: Optional[datetime] = Field(
        None,
        description='Срок выполнения',
    )

    @model_validator(mode='before')
    @classmethod
    def validate_and_clean_fields(cls, data: dict) -> dict:
        if 'description' in data and (
            data['description'] == '' or data['description'] is None
        ):
            data['description'] = None

        deadline_val = data.get('deadline')

        if deadline_val == '' or deadline_val is None:
            data['deadline'] = None
        else:
            if isinstance(deadline_val, str):
                try:
                    if 'T' in deadline_val:
                        dt = datetime.strptime(deadline_val, '%Y-%m-%dT%H:%M')
                    else:
                        dt = datetime.strptime(deadline_val, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Неверный формат даты')
            else:
                dt = deadline_val
            if dt and dt < datetime.now():
                raise ValueError('Срок выполнения не может быть в прошлом')

            data['deadline'] = dt
        return data


class Tasks(BaseModel):
    tasks: List[Task]
