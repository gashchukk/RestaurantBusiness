import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


def test_login(client: TestClient, test_employee):
    """Test login endpoint"""
    # Test successful login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_employee.email,
            "password": "password",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    # Test invalid password
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": test_employee.email,
            "password": "wrong-password",
        },
    )
    assert response.status_code == 401
    assert "detail" in response.json()
    
    # Test non-existent user
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password",
        },
    )
    assert response.status_code == 401
    assert "detail" in response.json()