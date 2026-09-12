from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login(payload):
    return {"status": "ok", "version": "1.0.0"}