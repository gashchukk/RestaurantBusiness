from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User, UserRole
from app.crud.restaurant import restaurant_crud
from app.schemas.restaurant import Restaurant, RestaurantCreate, RestaurantUpdate

router = APIRouter()


def check_restaurant_owner_role(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Check if the current user has restaurant owner or admin role
    """
    if current_user.role not in [UserRole.RESTAURANT_OWNER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Need to be restaurant owner or admin.",
        )
    return current_user


@router.post("/", response_model=Restaurant)
def create_restaurant(
    *,
    db: Session = Depends(get_db),
    restaurant_in: RestaurantCreate,
    current_user: User = Depends(check_restaurant_owner_role),
) -> Any:
    """
    Create new restaurant
    """
    restaurant = restaurant_crud.create_with_owner(
        db=db, obj_in=restaurant_in, owner_id=current_user.id
    )
    return restaurant


@router.get("/", response_model=List[Restaurant])
def read_restaurants(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve restaurants
    """
    restaurants = restaurant_crud.get_multi(db, skip=skip, limit=limit)
    return restaurants


@router.get("/owned", response_model=List[Restaurant])
def read_owned_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_restaurant_owner_role),
) -> Any:
    """
    Retrieve owned restaurants
    """
    return restaurant_crud.get_by_owner(db=db, owner_id=current_user.id)


@router.get("/{id}", response_model=Restaurant)
def read_restaurant(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get restaurant by ID
    """
    restaurant = restaurant_crud.get(db=db, id=id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    return restaurant


@router.put("/{id}", response_model=Restaurant)
def update_restaurant(
    *,
    db: Session = Depends(get_db),
    id: int,
    restaurant_in: RestaurantUpdate,
    current_user: User = Depends(check_restaurant_owner_role),
) -> Any:
    """
    Update a restaurant
    """
    restaurant = restaurant_crud.get(db=db, id=id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    
    # Only owner or admin can update
    if restaurant.owner_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    restaurant = restaurant_crud.update(
        db=db, db_obj=restaurant, obj_in=restaurant_in
    )
    return restaurant