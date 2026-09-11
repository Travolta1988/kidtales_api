from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Fairytale AI API",
    description="API for fairy tales AI interactive generation",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")