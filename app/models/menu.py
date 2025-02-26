from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
import datetime

from app.db.base import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date, index=True, nullable=False)
    items = Column(JSON, nullable=False)  # Stores menu items as JSON
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="menus")
    votes = relationship("Vote", back_populates="menu")