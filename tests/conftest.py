import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.core.config import settings
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.db.session import engine
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    # Clean up dependency override
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def test_admin(db_session):
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
    
    return admin


@pytest.fixture(scope="function")
def test_employee(db_session):
    """Create test employee user"""
    employee = User(
        email="employee@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Test Employee",
        role=UserRole.EMPLOYEE,
        is_active=True
    )
    
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    
    return employee


@pytest.fixture(scope="function")
def test_restaurant_owner(db_session):
    """Create test restaurant owner user"""
    owner = User(
        email="restaurant_owner@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Test Restaurant Owner",
        role=UserRole.RESTAURANT_OWNER,
        is_active=True
    )
    
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)
    
    return owner


@pytest.fixture(scope="function")
def admin_token(client, test_admin):
    """Get admin token"""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_admin.email,
            "password": "password",
        },
    )
    
    token = response.json()["access_token"]
    return token


@pytest.fixture(scope="function")
def employee_token(client, test_employee):
    """Get employee token"""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_employee.email,
            "password": "password",
        },
    )
    
    token = response.json()["access_token"]
    return token


@pytest.fixture(scope="function")
def restaurant_owner_token(client, test_restaurant_owner):
    """Get restaurant owner token"""
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_restaurant_owner.email,
            "password": "password",
        },
    )
    
    token = response.json()["access_token"]
    return token

print("conftest_postgres.py loaded!")
