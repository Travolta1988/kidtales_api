from fastapi import APIRouter
from app.api.v1.endpoints import stories, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health Check"])
api_router.include_router(stories.router, prefix="/stories", tags=["Stories"])