<#
AIOFFICE LOADTEST PLAYBOOK (User, PowerShell 7+, .venv Active)

Цель:
- Нагрузочно прогнать aioffice-probe (observability.metrics_app) локально.
- Проверить стабильность /healthz и /metrics под параллельной нагрузкой.
- Зафиксировать latency и error rate.

ПРЕДУСЛОВИЕ ВРУЧНУЮ (ОЧЕНЬ ВАЖНО):
1. В отдельной сессии PowerShell 7 (.venv Active) поднять сервис-пробку:
   cd C:\work\AICORPORATION\AIOFFICE
   uvicorn observability.metrics_app:app --host 127.0.0.1 --port 8001
   (он должен слушать http://127.0.0.1:8001)

2. В новой сессии PowerShell 7 (.venv Active, контекст User) запустить ЭТОТ скрипт.

Что делает сам скрипт:
- Запускает locust в headless-режиме:
    - --users : сколько одновременных виртуальных клиентов
    - --spawn-rate : с какой скоростью их добавлять
    - --run-time : сколько держать нагрузку
- Пишет агрегированные метрики в консоль (включая RPS, среднюю латентность, ошибки).

ВАЖНО:
- Это ТОЛЬКО локальный стресс-тест.
- Не бьём продуктивный сервис.
- Не запускаем под Administrator.
- Результаты теста сохраняем вручную (копируем вывод в отчёт по нагрузочным тестам).

Пример интерпретации результатов:
- Если /healthz даёт ошибки HTTP 5xx под нагрузкой <= N юзеров => это деградация доступности.
- Если p95 latency /healthz > 200ms при лёгкой нагрузке => нужно расследовать.
- Если /metrics начинает падать => мониторинг сам по себе может быть точкой отказа.

Команда запуска Locust:
#>

Write-Host "Starting locust headless load test against aioffice probe at http://127.0.0.1:8001 ..." -ForegroundColor Yellow

locust `
    --headless `
    --users 50 `
    --spawn-rate 10 `
    --run-time 30s `
    --host http://127.0.0.1:8001 `
    -f .\loadtest\locustfile.py
