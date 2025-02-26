from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router as api_router_v1
from app.api.v2.router import api_router as api_router_v2
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Lunch Decision API for company employees"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API version handling middleware
@app.middleware("http")
async def api_version_middleware(request: Request, call_next):
    app_version = request.headers.get("app-version", "v1")
    
    # Set the version in request state for later use
    request.state.version = app_version
    
    response = await call_next(request)
    return response

# Include routers for different API versions
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
app.include_router(api_router_v2, prefix=settings.API_V2_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Lunch Decision API"}