# Code Security Policy — CORPORATION / OFFICE

## Общие правила
- Запрет на секреты в репозитории (пароли, токены, ключи) — хранить в **Windows Credential Manager**.
- Запрет на старое имя проекта «Director» — используем «CORPORATION / OFFICE».
- Обязательны линтеры/сканеры: **ruff**, **bandit**, проверка в CI.
- Юнит-тесты не должны выполнять админские команды; **PowerShell-блоки не допускаются** в Python-тестах.

## Python
- Версия: 3.11, зависимости фиксировать в `requirements*.txt`.
- Безопасные библиотеки для криптографии/JWT: `python-jose[cryptography]`.
- Логи только в JSON, без PII (допустим `sub`).

## Конфигурации и секреты
- `.env` хранится локально/на сервере, НЕ в git; пример — `.env.example`.
- Ротация секретов по `ops/secrets_rotation_schedule.yaml`.

## CI/CD
- Блокировать merge при падении ruff/bandit/pytest.
- Сборка Docker-образа только из проверенных зависимостей.

## Инциденты
- Все нарушения — через постмортем `ops/incident_postmortem_template.md`.

Подпись владельца политики: __________________  Дата: __________
