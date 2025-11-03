# apps/backend_core/health.py — unified health router
import time
import socket
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()
START_TIME = time.time()

@router.get("/healthz", summary="Liveness probe (always 200)")
async def healthz() -> dict:
    # Не проверяем внешние зависимости — только факт живого процесса
    return {"status": "ok"}

@router.get("/health", summary="Process liveness + basic info")
async def health() -> dict:
    uptime_seconds = time.time() - START_TIME
    return {
        "status": "ok",
        "uptime_sec": round(uptime_seconds, 2),
    }

def _check_redis_tcp(host: str = "127.0.0.1", port: int = 6379, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

@router.get("/ready", summary="Readiness (deps must be up)")
async def ready():
    redis_ok = _check_redis_tcp()
    if redis_ok:
        return {"ready": True, "deps": {"redis_tcp": True}}
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"ready": False, "deps": {"redis_tcp": False}},
    )
