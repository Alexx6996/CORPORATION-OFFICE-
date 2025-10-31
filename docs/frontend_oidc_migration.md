# Frontend OIDC Migration Guide — CORPORATION / OFFICE

## Цель
Перевести фронтенд на OIDC Authorization Code Flow с PKCE. Бэкенд уже поддерживает Bearer JWT (см. /auth/whoami) и аварийный откат на BasicAuth.

## Провайдер (заполнить конкретику)
- Issuer: ${OIDC_ISSUER}
- Client ID: ${OIDC_CLIENT_ID}
- Redirect URIs:
  - http://localhost:3000/oidc/callback
  - https://staging.example/oidc/callback
  - https://app.example/oidc/callback
- Post-logout Redirect URIs:
  - http://localhost:3000/
  - https://app.example/

## Поток авторизации (Code + PKCE)
1) Генерация code_verifier + code_challenge (S256) на клиенте.
2) Редирект на `${OIDC_AUTH_URL}?client_id=...&redirect_uri=...&response_type=code&scope=openid profile email&code_challenge=...&code_challenge_method=S256&state=...`.
3) На /oidc/callback обмен кода на токены через `${OIDC_TOKEN_URL}` (через фронт-бэк прокси/серверную функцию, **не** с клиентского секрета).
4) Хранение токенов: **in-memory** или secure httpOnly cookie (предпочтительно), не localStorage.
5) Обновление: refresh token вращается через бэк (или iframe/hidden fetch — зависит от провайдера).
6) Добавлять `Authorization: Bearer <access_token>` к вызовам бекенда.

## Безопасность
- Часы синхронизированы (drift < 60s).
- Проверять `iss`, `aud` (если задан), `exp`, `nbf`.
- CSRF защита на callback: проверка `state`.
- PII в логах не писать (кроме `sub` как user_id).

## Откат (rollback)
- ENV на бэке: `AUTH_ROLLBACK_TO_BASIC=true`.
- Фронт: временно отключить OIDC-редирект, отправлять Basic в dev-профиле (только на внутренних стендах).
- Вернуться к OIDC после устранения причины (JWKS/часовой дрейф/настройки клиента).

## Чек-лист Staging
- [ ] Логин/логаут проходит end-to-end.
- [ ] Запросы к API с Bearer JWT дают 200, без токена — 401/403.
- [ ] /auth/whoami возвращает `auth=oidc`.
- [ ] Обновление access token работает (silent refresh / RT через бэк).
- [ ] Ошибочные/просроченные токены → корректная переаутентификация.

## Чек-лист Prod
- [ ] Бэкап и план отката готовы.
- [ ] Метрики авторизации/401/403 отслеживаются (alerts.yaml).
- [ ] 24 часа наблюдения: 5xx < 1%, жалоб нет.

Сопутствующие документы:
- `adr/ADR-0001-oidc-migration.md`
- `.env.example` (OIDC_*, AUTH_ROLLBACK_TO_BASIC)
