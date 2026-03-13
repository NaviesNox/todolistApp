from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    description: str = Field(min_length=1, max_length=5000)
    deadline: datetime


class TaskUpdate(BaseModel):
    description: str = Field(min_length=1, max_length=5000)
    deadline: datetime


class TaskRead(BaseModel):
    id: int
    description: str
    deadline: datetime
    created_at: datetime
    updated_at: datetime

