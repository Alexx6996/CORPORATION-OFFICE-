# tests/test_fiscal.py
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Монтируем fiscal-роутер (использует общую зависимость авторизации)
from integrations.fiscal.router import router as fiscal_router

def make_app():
    app = FastAPI()
    app.include_router(fiscal_router)
    return app

def test_fiscal_health():
    client = TestClient(make_app())
    r = client.get("/fiscal/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_fiscal_emit_basic_ok(monkeypatch):
    # Форсируем Basic fallback
    monkeypatch.setenv("AUTH_ROLLBACK_TO_BASIC", "true")
    monkeypatch.setenv("BASICAUTH_USER", "u")
    monkeypatch.setenv("BASICAUTH_PASS", "p")
    client = TestClient(make_app())
    r = client.post("/fiscal/emit", json={"order_id": "ORD-1", "amount": 10}, auth=("u", "p"))
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "created"
    assert body["receipt_id"].startswith("rcpt_")

def test_fiscal_emit_validation(monkeypatch):
    monkeypatch.setenv("AUTH_ROLLBACK_TO_BASIC", "true")
    monkeypatch.setenv("BASICAUTH_USER", "u")
    monkeypatch.setenv("BASICAUTH_PASS", "p")
    client = TestClient(make_app())
    r = client.post("/fiscal/emit", json={"order_id": "ORD-2", "amount": 0}, auth=("u", "p"))
    assert r.status_code == 400
