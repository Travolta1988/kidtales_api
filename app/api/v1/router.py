from fastapi import APIRouter
from app.api.v1.endpoints import stories, health, auth

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health Check"])
api_router.include_router(stories.router, prefix="/stories", tags=["Stories"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])