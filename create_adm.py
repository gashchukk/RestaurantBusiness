from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.core.config import settings
from app.models.user import User, UserRole
from app.core.security import get_password_hash


def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = TestSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
    # Drop all tables after test completes
    Base.metadata.drop_all(bind=engine)

def admin(db_session):
    """Create test admin user"""
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Test Admin",
        role=UserRole.ADMIN,
        is_active=True
    )
    
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    print(admin)
    return admin

admin(db_session)