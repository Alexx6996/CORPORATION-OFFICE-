# AIOFFICESSvc — профиль службы
Дата ревизии: 2025-10-29
Источник фактов: opsreport_operational_baseline_2025-10-29.md

## 1. Назначение
AIOFFICESSvc — это Windows-служба, которая поднимает ядро CORPORATION / OFFICE (FastAPI + uvicorn)
и делает его доступным локально на 127.0.0.1:8181.
Сервис — сердцевина узла. Без него система не считается "в эксплуатации".

## 2. Запуск (NSSM)
Служба управляется через NSSM (Non-Sucking Service Manager).
NSSM следит за процессом uvicorn и перезапускает его, если он падает.

### 2.1 Основные поля NSSM
- Service name: AIOFFICESSvc
- AppDirectory:
  C:\work\AICORPORATION\AIOFFICE
- Application (python.exe внутри .venv):
  C:\work\AICORPORATION\AIOFFICE\.venv\Scripts\python.exe
- AppParameters:
  -m uvicorn apps.backend_core.main:app --host 127.0.0.1 --port 8181 --log-level info

### 2.2 Логи службы
- Основной лог uvicorn/stdout/stderr через NSSM:
  C:\work\AICORPORATION\AIOFFICE\observability\aiofficessvc.log
- Лог запуска лаунчера / рестартов службы:
  C:\work\AICORPORATION\AIOFFICE\observability\launcher_aiofficessvc.log

Требование: директория observability\ должна быть доступна на запись учётке,
под которой крутится служба (см. Раздел 4).

### 2.3 Политика рестартов (NSSM)
- Start: Automatic
- Restart delay: 5s
- Restart on unexpected exit: Yes
- Stop method: graceful (Ctrl+C / SIGINT эквивалент для uvicorn)
- AppExit: процесс uvicorn обязан быть long-running. Любой выход != 0 — авария.

## 3. Сетевые допущения
- uvicorn слушает только 127.0.0.1:8181.
- Прямой внешний доступ к uvicorn запрещён.
- Внешний доступ (если нужен) идёт через reverse proxy с аутентификацией.
- Файрвол не должен пускать трафик к ядру извне, только с localhost.

## 4. Учётная запись службы
Целевое состояние PROD:
- Account: NT AUTHORITY\LocalService
- Права на код и окружение (C:\work\AICORPORATION\AIOFFICE и .venv\): только Read & Execute (RX).
- Права на директорию логов observability\: Modify (M), чтобы писать aiofficessvc.log и launcher_aiofficessvc.log.
- Служба не должна иметь права модифицировать исходный код, миграции, секреты и т.д.

## 5. Мониторинг живости
Служба обязана обеспечивать доступность следующих эндпоинтов FastAPI ядра CORPORATION / OFFICE:
- /health    → процесс жив, HTTP 200
- /ready     → готовность ядра и зависимостей (Redis и т.д.)
- /version   → версионированный билд, чтобы оператор видел что сейчас крутится
- /metrics   → метрики Prometheus для наблюдаемости

Эти же проверки вызывает ops_routines\start-day.ps1.

## 6. Версионирование
Версия ядра CORPORATION / OFFICE берётся из version.txt (или git hash)
и должна отражаться в /version.
Оператор узнаёт текущую версию узла по сети без входа на хост.

---
