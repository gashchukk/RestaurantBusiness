import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_restaurant(client: TestClient, restaurant_owner_token):
    """Test create restaurant endpoint"""
    headers = {"Authorization": f"Bearer {restaurant_owner_token}"}
    restaurant_data = {
        "name": "Test Restaurant",
        "address": "123 Test Street",
        "description": "A test restaurant"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/restaurants/",
        headers=headers,
        json=restaurant_data,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == restaurant_data["name"]
    assert data["address"] == restaurant_data["address"]
    assert data["description"] == restaurant_data["description"]
    assert "id" in data
    assert "owner_id" in data
    
    # Store restaurant ID for later tests
    restaurant_id = data["id"]
    
    # Test get restaurant by ID
    response = client.get(
        f"{settings.API_V1_STR}/restaurants/{restaurant_id}",
        headers=headers,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == restaurant_data["name"]
    
    # Test get all restaurants
    response = client.get(
        f"{settings.API_V1_STR}/restaurants/",
        headers=headers,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(r["id"] == restaurant_id for r in data)
    
    # Test update restaurant
    update_data = {
        "name": "Updated Restaurant Name"
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/restaurants/{restaurant_id}",
        headers=headers,
        json=update_data,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["address"] == restaurant_data["address"]  # Unchanged