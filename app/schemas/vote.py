from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.restaurant import Restaurant
from app.schemas.menu import Menu


class VoteBase(BaseModel):
    menu_id: int


class VoteCreate(VoteBase):
    pass


class VoteInDBBase(VoteBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Vote(VoteInDBBase):
    pass


class VoteResult(BaseModel):
    restaurant: Restaurant
    menu: Menu
    votes_count: int