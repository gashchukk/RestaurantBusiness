from typing import List, Optional, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.crud.base import CRUDBase
from app.models.vote import Vote
from app.models.menu import Menu
from app.models.restaurant import Restaurant
from app.schemas.vote import VoteCreate


class CRUDVote(CRUDBase[Vote, VoteCreate, VoteCreate]):
    def get_by_user_and_day(self, db: Session, *, user_id: int, day: date) -> Optional[Vote]:
        """ Get a user's vote for a specific day """
        return (
            db.query(Vote)
            .join(Menu)
            .filter(Vote.user_id == user_id, Menu.day == day)
            .first())

    def create_user_vote( self, db: Session, *, obj_in: VoteCreate, user_id: int) -> Vote:
        """ Create a new vote for a user, replacing any existing vote for the day """
        # Get the menu to determine the day
        menu = db.query(Menu).filter(Menu.id == obj_in.menu_id).first()
        if not menu:
            raise ValueError("Menu not found")
        
        # Check if user already voted for this day
        existing_vote = self.get_by_user_and_day(db=db, user_id=user_id, day=menu.day)
        
        # If already voted, update the existing vote
        if existing_vote:
            existing_vote.menu_id = obj_in.menu_id
            db.add(existing_vote)
            db.commit()
            db.refresh(existing_vote)
            return existing_vote
        
        # Otherwise create a new vote
        db_obj = Vote(
            user_id=user_id,
            menu_id=obj_in.menu_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_vote_results_for_day(self, db: Session, *, day: date) -> List[Dict[str, Any]]:
        """ Get voting results for a specific day, with counts by restaurant/menu """
        results = (
            db.query(
                Menu, 
                Restaurant,
                func.count(Vote.id).label("vote_count")
            )
            .join(Vote, Vote.menu_id == Menu.id, isouter=True)
            .join(Restaurant, Menu.restaurant_id == Restaurant.id)
            .filter(Menu.day == day)
            .group_by(Menu.id, Restaurant.id)
            .order_by(desc("vote_count"))
            .all()
        )
        
        return results


vote_crud = CRUDVote(Vote)