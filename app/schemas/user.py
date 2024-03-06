from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    id: int
    name: str
    description: str


class UserFullInfo(BaseModel):
    id: int
    name: str
    description: str
    date_create: datetime
    date_update: Optional[datetime]


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=5, max_length=100)


