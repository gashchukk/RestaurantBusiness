from typing import Any, List
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.crud.vote import vote_crud
from app.crud.menu import menu_crud
from app.schemas.vote import Vote, VoteCreate, VoteResult

router = APIRouter()


@router.post("/", response_model=Vote)
def create_vote(
    *,
    db: Session = Depends(get_db),
    vote_in: VoteCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Vote for a menu
    """
    # Verify menu exists
    menu = menu_crud.get(db=db, id=vote_in.menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found",
        )
    
    # Make sure menu is for current day
    today = date.today()
    if menu.day != today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only vote for today's menu",
        )
    
    # Create or update vote
    return vote_crud.create_user_vote(
        db=db, 
        obj_in=vote_in, 
        user_id=current_user.id
    )


@router.get("/me/today", response_model=Vote)
def read_my_vote(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's vote for today
    """
    today = date.today()
    vote = vote_crud.get_by_user_and_day(
        db=db, 
        user_id=current_user.id, 
        day=today
    )
    
    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No vote found for today",
        )
    
    return vote


@router.get("/results/today", response_model=List[dict])
def get_today_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get voting results for today
    """
    today = date.today()
    results = vote_crud.get_vote_results_for_day(db=db, day=today)
    
    # Convert SQLAlchemy objects to dictionaries
    formatted_results = []
    for menu, restaurant, vote_count in results:
        formatted_results.append({
            "restaurant": restaurant,
            "menu": menu,
            "votes_count": vote_count
        })
    
    return formatted_results