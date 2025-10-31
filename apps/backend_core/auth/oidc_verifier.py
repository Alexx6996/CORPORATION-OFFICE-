# apps/backend_core/auth/oidc_verifier.py
from __future__ import annotations

import os
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic, HTTPBasicCredentials

from .oidc_config import DEFAULT as OIDC

# Security schemes
_bearer = HTTPBearer(auto_error=False)
_basic = HTTPBasic(auto_error=False)

class AuthUser(Dict[str, Any]):
    """Простая модель пользователя на базе клеймов/учётки."""

def _basic_auth(creds: Optional[HTTPBasicCredentials]) -> AuthUser:
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Basic credentials required")
    user = os.getenv("BASICAUTH_USER", "")
    pw = os.getenv("BASICAUTH_PASS", "")
    if not user or not pw:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="BasicAuth not configured")
    if creds.username != user or creds.password != pw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Basic credentials")
    return AuthUser(sub=creds.username, auth="basic")

def _oidc_auth(token: Optional[HTTPAuthorizationCredentials]) -> AuthUser:
    if token is None or token.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    # Жёсткий контракт: когда OIDC включён — проверяем JWT через python-jose и JWKS.
    try:
        from jose import jwk, jwt
        from jose.utils import base64url_decode  # noqa: F401
    except Exception as e:  # jose не установлен
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="OIDC not available (jose missing)") from e

    # Минимальная проверка подписи через JWKS (без сетевых вызовов здесь).
    # Реальная загрузка/кэш JWKS должна выполняться в слое инициализации приложения.
    # Здесь — безопасный фолбек: если JWKS не задан, отклоняем запрос.
    jwks_url = OIDC.jwks_url
    if not jwks_url:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="JWKS URL not configured")

    # NOTE: чтобы не тянуть сеть в рантайме зависимости, ожидаем, что приложение
    # заполняет кэш JWKS в app.state. Если кэша нет — 503.
    # app.state.oidc_jwks = {"keys": [...]}
    def _get_jwks_from_request(req: Request) -> Dict[str, Any]:
        jwks = getattr(req.app.state, "oidc_jwks", None)
        if not jwks:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="JWKS cache not loaded")
        return jwks

    def _verify_with_jwks(req: Request, tok: str) -> Dict[str, Any]:
        headers = jwt.get_unverified_header(tok)
        kid = headers.get("kid")
        jwks = _get_jwks_from_request(req)
        key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
        if not key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown token kid")
        # Верификация и декод с проверкой iss/aud
        options = {"verify_aud": bool(OIDC.audience)}
        claims = jwt.decode(
            tok,
            key,
            algorithms=[key.get("alg", "RS256")],
            audience=OIDC.audience,
            issuer=OIDC.issuer,
            options=options,
        )
        return claims

    # Функция-обёртка для FastAPI зависимости — нужен Request для доступа к app.state
    def _verify(request: Request) -> AuthUser:
        claims = _verify_with_jwks(request, token.credentials)
        return AuthUser(**claims, auth="oidc")

    # Возвращаем вложенную зависимость, FastAPI сам пробросит Request
    return _verify  # type: ignore[return-value]

async def get_current_user(
    request: Request,
    bearer: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
    basic: Optional[HTTPBasicCredentials] = Depends(_basic),
) -> AuthUser:
    """
    Единая точка входа авторизации:
    - Если включён аварийный откат или OIDC выключен — используем BasicAuth.
    - Иначе — строгий OIDC (Bearer + JWKS).
    """
    if OIDC.rollback_to_basic or not OIDC.enabled:
        return _basic_auth(basic)

    verifier = _oidc_auth(bearer)
    if callable(verifier):
        # Когда OIDC включён, _oidc_auth вернёт функцию-проверку, требующую Request.
        return verifier(request)  # type: ignore[misc]
    # Теоретически не достижимо
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Auth verifier misconfigured")
