from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuUpdate


class CRUDMenu(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    def get_by_restaurant_and_day(
        self, db: Session, *, restaurant_id: int, day: date
    ) -> Optional[Menu]:
        return (
            db.query(Menu)
            .filter(Menu.restaurant_id == restaurant_id, Menu.day == day)
            .first()
        )

    def get_by_day(
        self, db: Session, *, day: date
    ) -> List[Menu]:
        return db.query(Menu).filter(Menu.day == day).all()
    
    def get_current_day_menus(self, db: Session) -> List[Menu]:
        """Get all menus for the current day"""
        today = date.today()
        return self.get_by_day(db=db, day=today)


menu_crud = CRUDMenu(Menu)