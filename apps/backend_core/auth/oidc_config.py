# apps/backend_core/auth/oidc_config.py
from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class OIDCConfig:
    enabled: bool
    issuer: str
    client_id: str
    client_secret: str | None
    auth_url: str
    token_url: str
    jwks_url: str
    audience: str | None
    # Флаг «аварийного отката» — включить BasicAuth (DEV) вместо OIDC
    rollback_to_basic: bool = False

    @staticmethod
    def from_env(prefix: str = "OIDC_") -> "OIDCConfig":
        get = os.getenv
        enabled = (get(f"{prefix}ENABLED", "false").lower() == "true")
        return OIDCConfig(
            enabled=enabled,
            issuer=get(f"{prefix}ISSUER", ""),
            client_id=get(f"{prefix}CLIENT_ID", ""),
            client_secret=get(f"{prefix}CLIENT_SECRET"),
            auth_url=get(f"{prefix}AUTH_URL", ""),
            token_url=get(f"{prefix}TOKEN_URL", ""),
            jwks_url=get(f"{prefix}JWKS_URL", ""),
            audience=get(f"{prefix}AUDIENCE"),
            rollback_to_basic=(get("AUTH_ROLLBACK_TO_BASIC", "false").lower() == "true"),
        )

DEFAULT = OIDCConfig.from_env()
