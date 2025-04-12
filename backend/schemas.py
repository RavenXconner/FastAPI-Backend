from pydantic import BaseModel
from typing import Optional

# Base Pydantic model for ToDo
class ToDoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class ToDoCreate(ToDoBase):
    pass

class ToDoUpdate(ToDoBase):
    pass

class ToDoOut(ToDoBase):
    id: int

    class Config:
        orm_mode = True  # To allow ORM models to be converted to Pydantic models
