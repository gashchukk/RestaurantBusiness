from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_active_user
from app.models.user import User, UserRole
from app.crud.user import user_crud
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


def check_admin_role(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Check if the current user has admin role
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user


@router.post("/", response_model=UserSchema)
def create_employee(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(check_admin_role),
) -> Any:
    """
    Create new employee (requires admin role)
    """
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return user_crud.create(db=db, obj_in=user_in)


@router.get("/", response_model=List[UserSchema])
def read_employees(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(check_admin_role),
) -> Any:
    """
    Retrieve employees (requires admin role)
    """
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    # Filter to only return employees
    employees = [user for user in users if user.role == UserRole.EMPLOYEE]
    return employees


@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user
    """
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user information
    """
    return user_crud.update(db=db, db_obj=current_user, obj_in=user_in)