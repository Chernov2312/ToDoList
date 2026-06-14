from pydantic import BaseModel, Field
from typing import Optional, List
class Item(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=50, description="Название списка")
    descripton: Optional[str] = Field(..., min_length=3, max_length=250, description="Описание")
    tasks: List[dict] = Field(..., description='Список заданий')