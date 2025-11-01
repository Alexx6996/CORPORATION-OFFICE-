# STAGING CHECKLIST — CORPORATION / OFFICE

## 1) Подготовка
- [ ] Обновить `.env` (OIDC_* / AUTH_ROLLBACK_TO_BASIC / BASICAUTH_*)
- [ ] Проверить Docker Desktop (WSL2) — Running
- [ ] Сеть `aioffice-net` существует (external)

## 2) Деплой
- [ ] `docker compose -f docker-compose.staging.yml up -d --build` — PASS
- [ ] Контейнеры `aioffice-staging-app`, `aioffice-staging-redis` — Running

## 3) Смоки (API)
- [ ] `GET http://127.0.0.1:8001/healthz` ⇒ 200
- [ ] `GET http://127.0.0.1:8001/metrics` ⇒ 200 (Prometheus)
- [ ] `GET /version` ⇒ содержит версию из `version.txt`

## 4) Auth
- [ ] Fallback Basic (если AUTH_ROLLBACK_TO_BASIC=true): `GET /auth/whoami` с Basic ⇒ 200, `{"auth":"basic"}`
- [ ] OIDC (если включён): `GET /auth/whoami` с Bearer JWT ⇒ 200, `{"auth":"oidc"}`
- [ ] Без токена/кредов ⇒ 401/403

## 5) Payments (sandbox)
- [ ] `GET /payments/health` ⇒ 200
- [ ] `POST /payments/charge` (amount>0) c авторизацией ⇒ 200 `{status: created}`

## 6) Миграции БД
- [ ] Alembic доступен в контейнере: `alembic history | tail -n 10` ⇒ OK
- [ ] (если есть миграции) `alembic upgrade head` ⇒ PASS

## 7) Наблюдаемость/Логи
- [ ] Логи JSON с trace_id/span_id
- [ ] Алерты `observability/alerts.yaml` — без критов

## 8) Rollback (готовность)
- [ ] Откат авторизации: `AUTH_ROLLBACK_TO_BASIC=true` — задокументирован
- [ ] `docker compose ...` образ предыдущей версии — доступен/проверен

## Итог
- [ ] Готово к релизу по `prod_release_checklist.md`
Подписи: User ______ / Administrator ______ / Дата: ______
