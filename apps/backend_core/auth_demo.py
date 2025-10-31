import base64
import logging
import os
import uuid

from fastapi import APIRouter, HTTPException, Request, status
from jose import JWTError, jwt

ISSUER = os.getenv("AIOFFICE_JWT_ISSUER", "aioffice.local")
AUDIENCE = os.getenv("AIOFFICE_JWT_AUDIENCE", "aioffice-clients")


def _secret_from_env() -> bytes:
    sec_b64 = os.getenv("AIOFFICE_JWT_SECRET_B64")
    if not sec_b64:
        raise RuntimeError("JWT secret not set")
    return base64.b64decode(sec_b64)


def validate_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            _secret_from_env(),
            algorithms=["HS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"verify_exp": True},
        )
        return payload
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token",
        ) from err


def get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id") or str(uuid.uuid4())


router = APIRouter()


@router.get("/version")
def version():
    return {"version": os.getenv("AIOFFICE_VERSION", "dev")}


@router.get("/api/protected")
def protected(request: Request, token: str | None = None):
    rid = get_request_id(request)
    if not token:
        raise HTTPException(status_code=401, detail="missing_token")
    claims = validate_jwt(token)
    log = logging.getLogger("aioffice")
    log.info(
        "access_ok",
        extra={
            "request_id": rid,
            "sub": claims.get("sub"),
        },
    )
    return {"ok": True, "sub": claims.get("sub"), "request_id": rid}
