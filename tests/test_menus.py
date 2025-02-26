from fastapi.testclient import TestClient
from datetime import date

from app.core.config import settings


def test_menu_workflow(client: TestClient, restaurant_owner_token, db_session):
    """Test full menu workflow"""
    headers = {"Authorization": f"Bearer {restaurant_owner_token}"}
    
    # 1. Create a restaurant first
    restaurant_data = {
        "name": "Menu Test Restaurant",
        "address": "456 Test Blvd",
        "description": "Testing the menu functionality"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/restaurants/",
        headers=headers,
        json=restaurant_data,
    )
    
    assert response.status_code == 200
    restaurant_id = response.json()["id"]
    
    # 2. Create a menu for today
    today = date.today()
    menu_data = {
        "day": today.isoformat(),
        "restaurant_id": restaurant_id,
        "items": [
            {
                "name": "Test Burger",
                "description": "A delicious test burger",
                "price": 9.99
            },
            {
                "name": "Test Salad",
                "description": "A fresh test salad",
                "price": 7.99
            }
        ]
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/menus/",
        headers=headers,
        json=menu_data,
    )
    
    assert response.status_code == 200
    menu_id = response.json()["id"]
    
    # 3. Get today's menus
    response = client.get(
        f"{settings.API_V1_STR}/menus/current",
        headers=headers,
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) >= 1
    assert any(m["id"] == menu_id for m in data)
    
    # 4. Update the menu
    update_data = {
        "items": [
            {
                "name": "Updated Burger",
                "description": "An updated test burger",
                "price": 10.99
            },
            {
                "name": "Test Salad",
                "description": "A fresh test salad",
                "price": 7.99
            },
            {
                "name": "New Soup",
                "description": "A new test soup",
                "price": 5.99
            }
        ]
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/menus/{menu_id}",
        headers=headers,
        json=update_data,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    
    # 5. Test creating duplicate menu for the same day
    response = client.post(
        f"{settings.API_V1_STR}/menus/",
        headers=headers,
        json=menu_data,
    )
    
    assert response.status_code == 400  # Should fail