@echo off
REM CORPORATION / OFFICE — service_launcher.cmd (жёсткая изоляция PATH)

echo [%date% %time%] service_launcher starting uvicorn >> C:\work\AICORPORATION\AIOFFICE\observability\launcher_aiofficessvc.log

REM 1) Полная изоляция PATH: только venv и системные каталоги
set "PATH=C:\work\AICORPORATION\AIOFFICE\.venv\Scripts;C:\Windows\System32;C:\Windows"
set PYTHONNOUSERSITE=1
set PYLAUNCHER_NO_SEARCH=1

REM 2) Диагностика: какой python/uvicorn будут использованы
where python >> C:\work\AICORPORATION\AIOFFICE\observability\launcher_aiofficessvc.log 2>&1
where uvicorn >> C:\work\AICORPORATION\AIOFFICE\observability\launcher_aiofficessvc.log 2>&1

REM 3) Явный запуск интерпретатора из venv
C:\work\AICORPORATION\AIOFFICE\.venv\Scripts\python.exe -m uvicorn apps.backend_core.main:app --host 127.0.0.1 --port 8181 --log-level info

exit /b %ERRORLEVEL%