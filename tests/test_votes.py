import pytest
from fastapi.testclient import TestClient
from datetime import date

from app.core.config import settings
from app.models.restaurant import Restaurant
from app.models.menu import Menu


def test_voting_workflow(
    client: TestClient, 
    db_session, 
    employee_token, 
    restaurant_owner_token
):
    """Test full voting workflow"""
    owner_headers = {"Authorization": f"Bearer {restaurant_owner_token}"}
    employee_headers = {"Authorization": f"Bearer {employee_token}"}
    
    # 1. Create restaurants
    restaurants = []
    for i in range(2):
        restaurant_data = {
            "name": f"Restaurant {i+1}",
            "address": f"{i+1} Test Street",
            "description": f"Test restaurant {i+1}"
        }
        
        response = client.post(
            f"{settings.API_V1_STR}/restaurants/",
            headers=owner_headers,
            json=restaurant_data,
        )
        
        assert response.status_code == 200
        restaurants.append(response.json())
    
    # 2. Create menus for today
    today = date.today()
    menus = []
    
    for i, restaurant in enumerate(restaurants):
        menu_data = {
            "day": today.isoformat(),
            "restaurant_id": restaurant["id"],
            "items": [
                {
                    "name": f"Dish {j+1} from Restaurant {i+1}",
                    "description": f"Test dish {j+1}",
                    "price": 9.99 + j
                }
                for j in range(3)
            ]
        }
        
        response = client.post(
            f"{settings.API_V1_STR}/menus/",
            headers=owner_headers,
            json=menu_data,
        )
        
        assert response.status_code == 200
        menus.append(response.json())
    
    # 3. Vote for a menu
    vote_data = {
        "menu_id": menus[0]["id"]
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/votes/",
        headers=employee_headers,
        json=vote_data,
    )
    
    assert response.status_code == 200
    vote = response.json()
    assert vote["menu_id"] == menus[0]["id"]
    assert 'id' in vote
    print(vote)
    assert 'created_at' in vote