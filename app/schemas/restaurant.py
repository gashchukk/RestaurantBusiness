from typing import Optional
from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    description: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


class RestaurantInDBBase(RestaurantBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class Restaurant(RestaurantInDBBase):
    pass