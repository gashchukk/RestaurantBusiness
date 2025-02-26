from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, get_api_version
from app.models.user import User, UserRole
from app.crud.menu import menu_crud
from app.crud.restaurant import restaurant_crud
from app.schemas.menu import Menu, MenuCreate, MenuUpdate

router = APIRouter()


def check_restaurant_owner(restaurant_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user),) -> None:
    """ Check if current user is the owner of the restaurant """
    restaurant = restaurant_crud.get(db=db, id=restaurant_id)
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )
    
    if (restaurant.owner_id != current_user.id and 
        current_user.role != UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )


@router.post("/", response_model=Menu)
def create_menu(*, db: Session = Depends(get_db), menu_in: MenuCreate,
                current_user: User = Depends(get_current_active_user)) -> Any:
    """ Create new menu for a restaurant """
    # Check if user is restaurant owner
    check_restaurant_owner(
        restaurant_id=menu_in.restaurant_id, 
        db=db, 
        current_user=current_user
    )
    
    # Check if menu for this day already exists
    existing_menu = menu_crud.get_by_restaurant_and_day(
        db=db, 
        restaurant_id=menu_in.restaurant_id, 
        day=menu_in.day
    )
    
    if existing_menu:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Menu for this restaurant on {menu_in.day} already exists",
        )
    
    return menu_crud.create(db=db, obj_in=menu_in)


@router.get("/current", response_model=List[Menu])
def read_current_day_menus(db: Session = Depends(get_db)) -> Any:
    """ Get all menus for the current day """
    return menu_crud.get_current_day_menus(db=db)


@router.get("/{menu_id}", response_model=Menu)
def read_menu(*, db: Session = Depends(get_db), menu_id: int) -> Any:
    """ Get a specific menu by ID """
    menu = menu_crud.get(db=db, id=menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found",
        )
    return menu


@router.put("/{menu_id}", response_model=Menu)
def update_menu(*, db: Session = Depends(get_db), menu_id: int, menu_in: MenuUpdate,
                current_user: User = Depends(get_current_active_user)) -> Any:
    """ Update a menu """
    
    menu = menu_crud.get(db=db, id=menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found",
        )
    
    # Check if user is restaurant owner
    check_restaurant_owner(
        restaurant_id=menu.restaurant_id, 
        db=db, 
        current_user=current_user
    )
    
    menu = menu_crud.update(db=db, db_obj=menu, obj_in=menu_in)
    return menu