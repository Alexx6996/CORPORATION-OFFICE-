from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time

APP_NAME = "CORPORATION / OFFICE backend core"
START_TIME = time.time()

app = FastAPI(title=APP_NAME)

@app.get("/health")
def health():
    uptime_seconds = time.time() - START_TIME
    return {
        "status": "ok",
        "app": APP_NAME,
        "uptime_sec": round(uptime_seconds, 2),
    }

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
# --- ops endpoints (/version, /ready) ---
# Эти эндпоинты нужны эксплуатации (наблюдаемость, ревизия версии, readiness).

from fastapi import APIRouter
from typing import Dict

# reuse global app defined earlier in this file.
# Если app уже существует (FastAPI instance), добавляем маршруты на него напрямую.

@app.get("/version")
def get_version() -> Dict[str, str]:
    """
    Версия запущенного ядра CORPORATION / OFFICE.
    Используется для удалённой проверки "что сейчас крутится".
    """
    return {
        "app": "CORPORATION / OFFICE backend core",
        "version": "dev-2025-10-28",
        "service": "AIOFFICESSvc"
    }

@app.get("/ready")
def get_ready() -> Dict[str, bool]:
    """
    Readiness-проба.
    На первой итерации всегда true.
    В следующей ревизии сюда добавим проверку зависимостей (Redis ping и т.п.).
    """
    return {
        "ready": True
    }
