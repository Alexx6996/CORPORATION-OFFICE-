# tests/test_auth.py
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Монтируем только auth-модуль
from apps.backend_core.auth.bootstrap import mount_auth


def make_app():
    app = FastAPI()
    mount_auth(app)
    return app

def test_auth_health():
    client = TestClient(make_app())
    r = client.get("/auth/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_whoami_basic_ok(monkeypatch):
    # Форсируем DEV-режим: откат на BasicAuth
    monkeypatch.setenv("AUTH_ROLLBACK_TO_BASIC", "true")
    monkeypatch.setenv("BASICAUTH_USER", "u")
    monkeypatch.setenv("BASICAUTH_PASS", "p")
    client = TestClient(make_app())
    r = client.get("/auth/whoami", auth=("u", "p"))
    assert r.status_code == 200
    body = r.json()
    assert body["sub"] == "u"
    assert body["auth"] == "basic"

def test_whoami_basic_unauthorized(monkeypatch):
    monkeypatch.setenv("AUTH_ROLLBACK_TO_BASIC", "true")
    monkeypatch.setenv("BASICAUTH_USER", "u")
    monkeypatch.setenv("BASICAUTH_PASS", "p")
    client = TestClient(make_app())
    r = client.get("/auth/whoami")  # без кредов
    assert r.status_code == 401
