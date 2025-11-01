# ADR-0001: Переход с DEV BasicAuth на OIDC (Authorization Code + PKCE)

Дата: 2025-10-31  
Статус: Accepted  
Решение: Включить OIDC в проде и на staging; BasicAuth использовать только как аварийный фолбек.

## Контекст
- Сейчас DEV использует BasicAuth; фронтенд переходит на OIDC (Code+PKCE).
- Бэкенд уже поддерживает Bearer JWT и JWKS-кэш; есть /auth/whoami.
- Нужны чёткие параметры ENV и сценарий отката.

## Варианты
1) Оставить только BasicAuth — **отклонено** (нет SSO, нет MFA, риск).
2) Добавить OIDC Implicit — **отклонено** (устаревший поток).
3) Authorization Code + PKCE — **выбрано** (best practice для SPA/PKCE).

## Решение
- Используем Code Flow + PKCE. Источник конфигурации — `.env` (`OIDC_*`).
- В проде — `OIDC_ENABLED=true`, `AUTH_ROLLBACK_TO_BASIC=false`.
- На staging допускаем временный fallback: `AUTH_ROLLBACK_TO_BASIC=true`.

## Детали реализации
- Бэкенд: верификация `iss`, `exp`, `nbf`, (опционально `aud`).
- JWKS-кэш — периодическое обновление.
- Фронтенд: хранение токенов в httpOnly cookie или in-memory (не localStorage).
- Обновление токена: через бэкенд/refresh endpoint провайдера.
- Логи: без PII (можно `sub`), трассировка — trace_id/span_id.

## Безопасность
- Часы синхронизированы (дрейф < 60s).
- Секреты клиента — в Windows Credential Manager.
- Ротация секретов по `ops/secrets_rotation_schedule.yaml`.

## Откат
- Установить `AUTH_ROLLBACK_TO_BASIC=true`.
- Отключить редиректы OIDC на фронте, включить Basic только на внутренних стендах.
- После устранения инцидента вернуть OIDC и снять откат.

## Проверка/Принятие
- Чек-листы: `staging_checklist.md`, `release_acceptance_checklist.md`.
- Руководство фронта: `docs/frontend_oidc_migration.md`.

## Последствия
- + Безопасность (SSO/MFA), централизованная идентификация.
- + Улучшенная аудитируемость (JWT claims).
- – Сложнее отладка по сравнению с BasicAuth (но есть fallback).

Подписанты:
- Developer: __________________
- Security:  __________________
- Administrator: ______________
