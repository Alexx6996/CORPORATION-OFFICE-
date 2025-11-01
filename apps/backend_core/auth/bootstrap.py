from __future__ import annotations
import logging
# apps/backend_core/auth/bootstrap.py

import json
import os
from typing import Any

from fastapi import FastAPI

from .oidc_config import DEFAULT as OIDC
from .router import router as auth_router


def _load_jwks() -> dict[str, Any] | None:
    """
    Источники JWKS в порядке приоритета:
    1) OIDC_JWKS_JSON (полный JSON)
    2) OIDC_JWKS_FILE (путь к локальному файлу)
    3) OIDC_JWKS_URL  (URL) — НЕ загружаем здесь, чтобы не зависеть от сети на старте.
       URL должен быть загружен внешним инициализатором и положен в app.state.oidc_jwks.
    """
    raw = os.getenv("OIDC_JWKS_JSON")
    if raw:
        try:
            return json.loads(raw)
        except Exception as e:`r`n    logging.getLogger("aioffice").warning("[auth-bootstrap] suppressed exception: %s", e)
    path = os.getenv("OIDC_JWKS_FILE")
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None

def mount_auth(app: FastAPI) -> None:
    """
    Подключает /auth роутер и (если OIDC включён) пытается заполнить кэш JWKS.
    Безопасный фолбек — если JWKS не найден, зависимость вернёт 503 при запросах.
    """
    app.include_router(auth_router)
    if OIDC.enabled and not getattr(app.state, "oidc_jwks", None):
        jwks = _load_jwks()
        if jwks:
            app.state.oidc_jwks = jwks  # {"keys": [...]}


