# TRAINING PLAN — CORPORATION / OFFICE

## Роли и модули
- User: ежедневные проверки, базовые релизы по чеклистам, ведение постмортемов.
- Administrator: операционные процедуры (служба, Docker, бэкапы/DR, ротация секретов).
- DomainOwners: интеграции (платежи/фискалка), комплаенс и юр-контур.

## Учебные блоки
1) Observability: /healthz, /metrics, alerts.yaml (SLO/SLA).
2) Ops-скрипты: start-day.ps1, stop-day.ps1, secrets_check.ps1.
3) CI/CD: ci.yml, release.yml, prod_release_checklist.md, staging_checklist.md.
4) DR/Backups: backup/, C:\Secure\Backups\, restore dry-run.
5) Security: Credential Manager, ротация секретов, доступы.
6) Auth: OIDC vs Basic fallback, проверка /auth/whoami.
7) Интеграции: payments/webhook, receipt_model.yaml, тесты.

## Формат и критерии
- Формат: 2х2 часа воркшопы + практикум на staging.
- Критерии: выполнить чеклисты staging и release acceptance без ошибок.

## Материалы
- ops/runbook.md, release_*checklist.md, adr/ADR-0001-oidc-migration.md,
  integrations/*, legal/legal_draft.md, docs/frontend_oidc_migration.md
