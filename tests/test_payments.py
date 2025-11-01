# tests/test_payments.py
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Монтируем только payments-роутер (он тянет общую зависимость авторизации)
from integrations.payments.router import router as payments_router


def make_app():
    app = FastAPI()
    app.include_router(payments_router)
    return app

def test_health():
    client = TestClient(make_app())
    r = client.get("/payments/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_charge_unauthorized():
    # Без кредов должен быть 401
    client = TestClient(make_app())
    r = client.post("/payments/charge", json={"amount": 1000, "currency": "RUB"})
    assert r.status_code in (401, 403)

def test_charge_ok_basic(monkeypatch):
    # Форсируем DEV-фолбек на BasicAuth
    monkeypatch.setenv("AUTH_ROLLBACK_TO_BASIC", "true")
    monkeypatch.setenv("BASICAUTH_USER", "u")
    monkeypatch.setenv("BASICAUTH_PASS", "p")
    client = TestClient(make_app())
    r = client.post("/payments/charge", json={"amount": 1000, "currency": "RUB"}, auth=("u", "p"))
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in {"created", "succeeded"}
    assert body["id"].startswith("test_charge_")

def test_charge_validation_basic(monkeypatch):
    monkeypatch.setenv("AUTH_ROLLBACK_TO_BASIC", "true")
    monkeypatch.setenv("BASICAUTH_USER", "u")
    monkeypatch.setenv("BASICAUTH_PASS", "p")
    client = TestClient(make_app())
    r = client.post("/payments/charge", json={"amount": 0}, auth=("u", "p"))
    assert r.status_code == 400
