# PROD RELEASE CHECKLIST (aioffice)

## Preconditions
- version.txt обновлён (SemVer), CHANGELOG для версии готов.
- CI пройдён: ruff/bandit/pytest/docker build ✅ (.github/workflows/ci.yml).
- release_acceptance_checklist.md = PASS.
- Нет OVERDUE секретов (ops/secrets_rotation_schedule.yaml).
- DR-план и бэкапы актуальны (backup\).

## Steps
1) [Admin] Быстрый бэкап БД и артефактов → C:\Secure\Backups\<date>\
2) [Admin] Остановить prod-службу/контейнер aioffice (по runbook).
3) [Admin] Применить миграции: **alembic upgrade head** (в prod окружении).
4) [Admin] Запустить новую версию образа aioffice:<VERSION>.
5) [User] Smoke:
   - GET /healthz → 200
   - GET /metrics → 200
   - Locust smoke: 5–10 мин, <1% 5xx
6) [User] Мониторинг/алерты: нет критических срабатываний.
7) [User] Подтвердить релиз. Обновить release_bundle.md (артефакты/ссылки/подписи).

## Rollback (если шаг 5–6 не пройдены)
- Остановить текущую версию → запустить предыдущий образ aioffice:<PREV_VERSION>
- alembic downgrade -1 (если регламентом разрешено; иначе план отката по DR)
- Проверить /healthz, /metrics, алерты. Заполнить постмортем.

## Sign-off
- User: «версия принята» (дата/подпись)
- Administrator: «выполнил по чеклисту, трафик включён» (дата/подпись)
