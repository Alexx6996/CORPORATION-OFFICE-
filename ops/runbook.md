# OPS RUNBOOK — CORPORATION / OFFICE

## Общее
- Хост Windows, служба: **AIOFFICESSvc** ("CORPORATION / OFFICE Backend Service") под LocalService.
- Backend: uvicorn (apps.backend_core.main:app) на 127.0.0.1:8181.
- Логи: .\observability\aiofficessvc.log (ротация NSSM), .\logs\* (JSON с trace_id/span_id).
- Метрики: GET http://127.0.0.1:8181/metrics
- Health:  GET http://127.0.0.1:8181/healthz

---

## Daily Checks (каждый день, утро)
1) Health/metrics:
   - `Invoke-WebRequest http://127.0.0.1:8181/healthz | % StatusCode` → **200**
   - `Invoke-WebRequest http://127.0.0.1:8181/metrics | % StatusCode` → **200**
2) Логи/алерты:
   - Просмотреть `observability\aiofficessvc.log`
   - Проверить алерты из `observability\alerts.yaml`
3) Redis/очереди:
   - `docker ps` — контейнер **aioffice-redis** в состоянии Up.
4) Секреты:
   - Проверить сроки в `ops\secrets_rotation_schedule.yaml` (нет OVERDUE/DUE_TODAY)

> Для автоматизации использовать `ops\start-day.ps1` и фиксировать RESULT: OK/ATTENTION.

---

## Старт/Стоп службы PROD
- **Старт:** `Start-Service AIOFFICESSvc`
- **Стоп:**  `Stop-Service AIOFFICESSvc`
- **Статус:** `Get-Service AIOFFICESSvc`

Если после старта /healthz ≠ 200 за 30 сек → собрать логи (`Get-Content -Tail 200 observability\aiofficessvc.log`) и эскалировать по SLO.

---

## Миграции БД (prod)
**Всегда перед включением трафика в релизе.**
1) Активируйте окружение/контейнер согласно чеклисту релиза.
2) Выполните: `alembic upgrade head`
3) Проверка:
   - `alembic current`
   - Прогон /healthz и smoke (раздел ниже)

> Dry-run/проверка истории миграций выполняется в CI и на staging. В prod — только **upgrade head** по чеклисту.

---

## Smoke-проверки (локально на хосте)
- `Invoke-WebRequest http://127.0.0.1:8181/healthz` → 200
- `Invoke-WebRequest http://127.0.0.1:8181/metrics` → 200
- Быстрый сценарий нагрузки (locust «smoke» 5–10 мин): <1% 5xx

---

## Rollback (откат)
- Вернуть предыдущий Docker-образ/билд согласно `prod_release_checklist.md`
- Если требуется, `alembic downgrade -1` **только** если разрешено регламентом и не нарушает целостность данных
- Повторить smoke и /healthz, зафиксировать постмортем

---

## Staging
- Up:   `docker compose -f docker-compose.staging.yml up -d --build`
- Down: `docker compose -f docker-compose.staging.yml down`
- Migrations: `docker exec -it aioffice-staging-app alembic upgrade head`
- Smoke: /healthz, /metrics, базовые пользовательские флоу

---

## Инциденты и эскалация
- S0: недоступность prod / утечка / критическая деградация SLA — немедленный созвон, останов релиза, возможен rollback
- S1–S3: по приоритету, в рабочее время, с трекингом в постмортем
- Шаблон: `ops\incident_postmortem_template.md` (указать impact, root cause, action items, owner, ETA)

---

## Секреты и сертификаты
- Фактические значения в **Windows Credential Manager** / BitLocker-хранилищах; в git — только метаданные сроков
- График: `ops\secrets_rotation_schedule.yaml`
- При DUE_SOON — плановая ротация; при OVERDUE — инцидент S0 Security

---

## Завершение дня
- Выполнить `ops\stop-day.ps1`: остановка службы, проверка Redis, итоговый статус.
- Архив аудита по дням сохранять в `observability\`.
