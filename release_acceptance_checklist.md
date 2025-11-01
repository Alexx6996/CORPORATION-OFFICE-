# RELEASE ACCEPTANCE CHECKLIST — CORPORATION / OFFICE

## 1) Предрелиз
- [ ] Версия: соответствует `version.txt` и тегу `vX.Y.Z`
- [ ] CI: зелёный (ruff, bandit, pytest, docker build)
- [ ] Чейнджлог/релизные заметки подготовлены
- [ ] Бэкапы в актуальном состоянии (см. backup/backup_policy.yaml)
- [ ] DR-план актуален (backup/dr_plan.yaml) — RTO/RPO подтверждены

## 2) Staging
- [ ] Пройден `staging_checklist.md` (все пункты OK)
- [ ] Alembic миграции проверены (`alembic upgrade head` на staging)
- [ ] Смоки API: `/healthz`=200, `/metrics`=200, `/auth/whoami`=200 (OIDC/или Basic fallback)
- [ ] Интеграции: payments (sandbox) → 200 `{status: created}`

## 3) Прод деплой
- [ ] Окно релиза и план отката согласованы (rollback образ/ENV готовы)
- [ ] Деплой образа X.Y.Z выполнен
- [ ] Alembic: `upgrade head` выполнен на прод
- [ ] Health&Metrics: `/healthz`=200, `/metrics`=200
- [ ] Логи без крит-ошибок за 15 минут после релиза

## 4) Auth (Prod)
- [ ] OIDC включён (`OIDC_ENABLED=true`, `AUTH_ROLLBACK_TO_BASIC=false`) ИЛИ подтверждён временный fallback
- [ ] Тестовый вход через фронт: PASS
- [ ] `/auth/whoami` возвращает `auth=oidc` (или `basic` при согласованном откате)

## 5) Наблюдение пост-релиза
- [ ] 2 часа: 5xx < 1%, latency в SLO (alerts.yaml)
- [ ] 24 часа: инцидентов S0/S1 нет

## 6) Юр/комплаенс
- [ ] legal/legal_draft.md актуализирован
- [ ] Политика кода/security согласованы (security/code_security_policy.md)

## Итог
- [ ] Релиз принят. Версия: ______ Дата/время: ______
Подписи: User ______ / Administrator ______ / Security ______
