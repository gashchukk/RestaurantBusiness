from fastapi import APIRouter

# In a real application, we'd have v2 endpoints here
# For now, this is just a placeholder to show how versioning works

api_router = APIRouter()

@api_router.get("/", status_code=200)
def root():
    """
    Root endpoint for API v2
    """
    return {
        "message": "Welcome to API v2",
        "status": "Not fully implemented yet, please use v1 endpoints"
    }