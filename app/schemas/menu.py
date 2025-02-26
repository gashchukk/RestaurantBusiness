from typing import Optional, List
from datetime import date
from pydantic import BaseModel


class MenuItem(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None


# V1 Menu Schemas
class MenuBase(BaseModel):
    day: date
    items: List[MenuItem]
    restaurant_id: int


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    day: Optional[date] = None
    items: Optional[List[MenuItem]] = None


class MenuInDBBase(MenuBase):
    id: int

    class Config:
        orm_mode = True


class Menu(MenuInDBBase):
    pass


# V2 Menu Schemas - Added categories
class MenuItemV2(MenuItem):
    category: Optional[str] = "Main"


class MenuBaseV2(BaseModel):
    day: date
    items: List[MenuItemV2]
    restaurant_id: int


class MenuCreateV2(MenuBaseV2):
    pass


class MenuV2(MenuBaseV2):
    id: int

    class Config:
        orm_mode = True