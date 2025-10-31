# RELEASE BUNDLE — CORPORATION / OFFICE

Version: 0.1.0
Build date: (заполнить при релизе)
Commit: (git sha)

## Артефакты
- Docker image: aioffice:0.1.0 (или registry/aioffice:0.1.0)
- Configs: .env (prod, НЕ в git), logging.yaml, app.yaml
- DB migrations: db/migrations (alembic)
- Observability: observability/alerts.yaml
- Checklists: prod_release_checklist.md, staging_checklist.md, release_acceptance_checklist.md
- Ops: ops/runbook.md, ops/start-day.ps1, ops/stop-day.ps1, ops/responsibility_matrix.yaml
- Legal: legal/legal_draft.md
- Integrations: integrations/payments/router.py, integrations/fiscal/receipt_model.yaml
- Auth: apps/backend_core/auth/* (OIDC/Basic fallback)

## Проверки перед публикацией
- CI: PASS (ruff/bandit/pytest/docker build)
- Staging: deploy + alembic upgrade head + smoke PASS
- Prod: бэкапы готовы; alembic upgrade head; /healthz, /metrics = 200; алерты OK

Подписи: User ______ / Administrator ______ / Дата: ______
