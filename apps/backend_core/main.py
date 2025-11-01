import os
import time

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

APP_NAME = "CORPORATION / OFFICE backend core"
START_TIME = time.time()

app = FastAPI(title=APP_NAME)

@app.get("/healthz")
@app.get("/health")
def healthz():
    return {"status": "ok"}


# -------------------------
# /health : liveness probe
# -------------------------
@app.get("/health")
def health():
    """
    Liveness-проба.
    Если это отвечает 200 -> процесс жив.
    Не гарантирует готовность зависимостей.
    """
    uptime_seconds = time.time() - START_TIME
    return {
        "status": "ok",
        "app": APP_NAME,
        "uptime_sec": round(uptime_seconds, 2),
    }

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
    2. git hash (TODO: реализовать в следующей ревизии)
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
    """
    Версия запущенного ядра CORPORATION / OFFICE.
    Используется оператором для инвентаризации удалённо.
    """
    return {
        "app": APP_NAME,
        "version": _read_version(),
        "service": "AIOFFICESSvc"
    }

# -------------------------
# /ready : readiness probe
# -------------------------
def _check_redis():
    """
    Пытается пингануть Redis.
    Если Redis недоступен -> бросаем исключение.
    """
    try:
        import redis  # требует redis-py в .venv
        client = redis.Redis(host="127.0.0.1", port=6379, db=0)
        # ping() вернёт True если всё ок, иначе кинет исключение
        return client.ping()
    except Exception:
        return False

@app.get("/ready")
def get_ready():
    """
    Readiness-проба:
    - True (HTTP 200)  -> сервис готов принимать трафик
    - False (HTTP 503) -> зависимость недоступна (например Redis)
    """
    redis_ok = _check_redis()

    ready = bool(redis_ok)

    if ready:
        return {"ready": True}
    else:
        # оператор должен увидеть, что сервис физически жив, но не готов
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "ready": False,
                "deps": {
                    "redis": bool(redis_ok),
                }
            }
        )

from apps.backend_core.auth_demo import router as auth_demo_router  # noqa: E402

app.include_router(auth_demo_router)

# --- AUTO-INJECT: AUTH BOOTSTRAP (CORPORATION / OFFICE) ---
try:
    from apps.backend_core.auth.bootstrap import mount_auth  # type: ignore
    mount_auth(app)  # подключает /auth и JWKS-кэш при включённом OIDC
except Exception as _e:  # не блокируем запуск при ошибке модуля авторизации
    # Логирование через стандартный print: основной лог подхватит stdout/stderr
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
@app.get("/healthz")
def healthz():
    return {"status": "ok"}


