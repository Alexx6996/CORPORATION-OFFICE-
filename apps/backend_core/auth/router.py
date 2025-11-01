# apps/backend_core/auth/router.py
from __future__ import annotations

from fastapi import APIRouter, Depends

from .oidc_verifier import AuthUser, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/health", summary="Auth module healthcheck")
async def health() -> dict:
    return {"status": "ok"}

@router.get("/whoami", summary="Return current user (secured)")
async def whoami(user: AuthUser = Depends(get_current_user)) -> dict:
    # Возвращаем минимум безопасной информации
    return {"sub": user.get("sub"), "auth": user.get("auth")}
