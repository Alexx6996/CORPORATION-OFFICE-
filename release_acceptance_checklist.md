# RELEASE ACCEPTANCE CHECKLIST — CORPORATION / OFFICE

## 1. Качество и безопасность
- [ ] Ruff/bandit/pytest в CI — PASS
- [ ] Статическая проверка секретов — PASS (нет утечек)
- [ ] Линтеры/политики (security/code_security_policy.md) — соблюдены

## 2. Наблюдаемость
- [ ] /healthz и /metrics — OK на staging
- [ ] Логи в JSON содержат trace_id/span_id
- [ ] Алерты (observability/alerts.yaml) — без критов

## 3. Данные и миграции
- [ ] Alembic migrations — применяются на staging (upgrade head)
- [ ] DR-план и бэкапы актуальны (backup/, C:\Secure\Backups\)

## 4. Интеграции
- [ ] Payments sandbox: /payments/health и /payments/charge — PASS (тесты)
- [ ] Фискальный контракт: receipt_model.yaml — заполнен и согласован (draft OK)

## 5. Юр-контур
- [ ] legal/legal_draft.md — базовый черновик готов
- [ ] Политика приватности/оферта — вынесены в документ, готовы к юр. ревизии

## 6. Операции (Ops)
- [ ] ops/runbook.md — заполнен (старт/стоп, миграции, откат, daily checks)
- [ ] ops/secrets_rotation_schedule.yaml — даты и статусы актуальны

## Итог
- [ ] Готов к prod-релизу по prod_release_checklist.md
Подписи: User ______ / Administrator ______ / Дата: ______
