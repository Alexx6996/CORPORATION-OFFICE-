import os
import time

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

APP_NAME = "CORPORATION / OFFICE backend core"
START_TIME = time.time()

app = FastAPI(title=APP_NAME)

# -------------------------
# /metrics : Prometheus
# -------------------------
@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# -------------------------
# /version : какой билд крутится
# -------------------------
def _read_version():
    """
    Возвращает строку версии, которую оператор должен видеть удалённо.
    Приоритет:
    1. version.txt в корне репозитория
    2. git hash (TODO)
    3. "unknown"
    """
    version_file = os.path.join(os.path.dirname(__file__), "..", "..", "version.txt")
    version_file = os.path.abspath(version_file)
    try:
        with open(version_file, encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return "unknown"

@app.get("/version")
def get_version():
    return {"app": APP_NAME, "version": _read_version(), "service": "AIOFFICESSvc"}

from apps.backend_core.auth_demo import router as auth_demo_router  # noqa: E402
app.include_router(auth_demo_router)

# --- AUTO-INJECT: AUTH BOOTSTRAP (CORPORATION / OFFICE) ---
try:
    from apps.backend_core.auth.bootstrap import mount_auth  # type: ignore
    mount_auth(app)
except Exception as _e:
    print(f"[auth-bootstrap] skipped: {_e}")
# --- /AUTO-INJECT ---

# --- AUTO-INJECT: PAYMENTS ROUTER (CORPORATION / OFFICE) ---
try:
    from integrations.payments.router import router as payments_router  # type: ignore
    app.include_router(payments_router)
except Exception as _e:
    print(f"[payments-bootstrap] skipped: {_e}")
# --- /AUTO-INJECT ---

# --- AUTO-INJECT: HEALTH ROUTER (CORPORATION / OFFICE) ---
try:
    from apps.backend_core.health import router as health_router  # type: ignore
    app.include_router(health_router)
except Exception as _e:
    print(f"[health-bootstrap] skipped: {_e}")
# --- /AUTO-INJECT ---

# --- AUTO-INJECT: METRICS ROUTER (CORPORATION / OFFICE) ---
try:
    from apps.backend_core.metrics import router as metrics_router  # type: ignore
    app.include_router(metrics_router)
except Exception as _e:
    print(f"[metrics-bootstrap] skipped: {_e}")
# --- /AUTO-INJECT ---

# --- AUTO-INJECT: FISCAL ROUTER (CORPORATION / OFFICE) ---
try:
    from integrations.fiscal.router import router as fiscal_router  # type: ignore
    app.include_router(fiscal_router)
except Exception as _e:
    print(f"[fiscal-bootstrap] skipped: {_e}")
# --- /AUTO-INJECT ---
