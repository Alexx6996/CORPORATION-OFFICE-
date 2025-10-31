# ADR-0001: Миграция аутентификации на OIDC (с аварийным откатом на BasicAuth)

## Статус
Accepted — 2025-10-31

## Контекст
Текущий DEV-режим использует BasicAuth. Для продакшна требуется стандартный OIDC с проверкой JWT по JWKS, ролевая модель (RBAC) и централизованная авторизация фронтенда.

## Решение
1) Бэкенд:
   - Модуль `apps/backend_core/auth/*`: конфиг `OIDC_*`, зависимость `get_current_user`, фолбек `AUTH_ROLLBACK_TO_BASIC=true`.
   - JWKS загружается при старте из ENV/файла (bootstrap) или заранее кладётся в `app.state.oidc_jwks`.
2) Фронтенд:
   - Использует OIDC Code Flow с PKCE; хранение токена в memory/secure storage; обновление через refresh token/iframe (зависит от провайдера).
3) Политики доступа:
   - Минимальная проверка клеймов (`sub`, `iss`, опционально `aud`), маппинг ролей будет добавлен отдельным ADR.
4) Observability:
   - В логи добавлять `sub` как user_id (PII SAFE), trace_id/span_id уже в системе.

## Конфигурация ENV (пример)
- `OIDC_ENABLED=true`
- `OIDC_ISSUER=https://issuer.example/`
- `OIDC_CLIENT_ID=...`
- `OIDC_CLIENT_SECRET=...`
- `OIDC_AUTH_URL=...`
- `OIDC_TOKEN_URL=...`
- `OIDC_JWKS_URL=...`
- `OIDC_AUDIENCE=...`
- `# Фолбек:` `AUTH_ROLLBACK_TO_BASIC=false`

## План миграции (этапы)
1) Staging:
   - Включить `OIDC_ENABLED=true`, разместить JWKS (ENV/файл), пройти /auth/health и e2e вход.
   - Smoke: защищённые эндпоинты требуют Bearer JWT; /auth/whoami возвращает `auth=oidc`.
2) Prod (по чеклистам релиза):
   - Бэкапы/DR → deploy → `alembic upgrade head` → включение OIDC.
   - Мониторинг 24ч: 5xx < 1%, нет аномалий авторизации.
3) Пост-миграция:
   - Выключить флаг отката (`AUTH_ROLLBACK_TO_BASIC=false`) после недели стабильной работы.

## План отката (rollback)
- Немедленно: `AUTH_ROLLBACK_TO_BASIC=true` (ENV), рестарт сервиса → BasicAuth.
- Проверки: /auth/whoami (Basic) → 200; бизнес-флоу не блокируется.
- Временные меры: отключить фронтовой OIDC редирект, включить Basic в dev-профиле.
- После стабилизации: найти причину (JWKS/время/дрейф клеймов), подготовить фикс, провести повторную миграцию через staging.

## Риски и смягчение
- Недоступность JWKS → 503 на /auth: смягчение — локальный JWKS-файл в BitLocker-хранилище.
- Дрейф часов/истечение токенов → 401: синхронизация времени, увеличенный допуск у провайдера.
- Несовместимость клеймов → валидацию/маппинг оформить отдельным ADR и тестами.

## Тест-кейсы
- DEV фолбек (Basic): `tests/test_auth.py` — PASS.
- OIDC: e2e на staging с реальным JWKS и валидным токеном (от провайдера), 401 при невалидном токене, 200 при валидном.

Автор(ы): User / Administrator
