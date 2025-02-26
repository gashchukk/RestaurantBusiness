from fastapi import APIRouter

from app.api.v1.endpoints import auth, restaurants, menus, employees, votes

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
