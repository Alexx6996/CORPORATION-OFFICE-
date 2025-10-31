# apps/backend_core/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz", summary="Liveness/health check")
async def healthz() -> dict:
    return {"status": "ok"}
