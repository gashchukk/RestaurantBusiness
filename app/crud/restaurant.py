from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class CRUDRestaurant(CRUDBase[Restaurant, RestaurantCreate, RestaurantUpdate]):
    def get_by_owner(self, db: Session, *, owner_id: int) -> List[Restaurant]:
        return db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()

    def create_with_owner(
        self, db: Session, *, obj_in: RestaurantCreate, owner_id: int
    ) -> Restaurant:
        db_obj = Restaurant(
            name=obj_in.name,
            address=obj_in.address,
            description=obj_in.description,
            owner_id=owner_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


restaurant_crud = CRUDRestaurant(Restaurant)