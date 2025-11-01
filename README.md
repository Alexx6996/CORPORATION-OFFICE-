# CORPORATION / OFFICE

[![CI](https://github.com/Alexx6996/CORPORATION-OFFICE-/actions/workflows/ci.yml/badge.svg)](https://github.com/Alexx6996/CORPORATION-OFFICE-/actions/workflows/ci.yml)

Локальная многоагентная платформа ИИ c FastAPI-ядром, наблюдаемостью (`/healthz`, `/metrics`), CI/CD и безопасной аутентификацией (OIDC с аварийным откатом на BasicAuth).

## Требования
- Windows 10/11, PowerShell 7+
- Docker Desktop (WSL2 backend)
- Python 3.11 (для локальной разработки)

## Быстрый старт (staging)
```powershell
docker compose -f docker-compose.staging.yml up -d --build
