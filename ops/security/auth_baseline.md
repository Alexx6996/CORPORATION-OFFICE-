# ADR-003: Auth Baseline (OIDC/JWT)
Дата: 2025-10-31
Решение: фронт — OIDC; бэкенд — JWT (issuer/aud/exp), роли RBAC; секреты — Windows Credential Manager; ротация по ops/secrets_rotation_schedule.yaml.
Имплементация: временно DEV-щит (Caddy BasicAuth), далее OIDC.
Риски: утечки секретов → хранить только в Credential Manager, запрет в git.

[2025-10-31] Caddy: basic_auth включён; security headers заданы; access-log → observability\caddy_access.log (JSON). Тесты /version=200, /api/protected: 401 без токена, 200 с валидным JWT — ОК.
