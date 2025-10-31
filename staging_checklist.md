# STAGING CHECKLIST (aioffice)

## Deploy
- docker compose -f docker-compose.staging.yml up -d --build
- Применить миграции: docker exec -it aioffice-staging-app alembic upgrade head

## Smoke
- /healthz → 200
- /metrics → 200
- Locust smoke: <1% 5xx, базовые сценарии чатов/очередей

## Gates
- Тесты интеграций (платежи sandbox / вебхуки) пройдены
- Фискальный контракт «чека» собран (dry-run)
- Логи содержат trace_id/span_id, алерты не срабатывают критически

## Output
- release_acceptance_checklist.md = PASS
