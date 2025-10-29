@echo off
REM CORPORATION / OFFICE
REM service_launcher.cmd
REM Назначение:
REM   - логируем запуск службы AIOFFICESSvc (включая автоперезапуски NSSM),
REM   - активируем .venv проекта,
REM   - запускаем uvicorn на 127.0.0.1:8181.

REM 1. Логируем факт старта (timestamp)
echo [%date% %time%] service_launcher starting uvicorn >> C:\work\AICORPORATION\AIOFFICE\observability\launcher_aiofficessvc.log

REM 2. Активируем виртуальное окружение проекта (.venv)
call C:\work\AICORPORATION\AIOFFICE\.venv\Scripts\activate.bat

REM 3. Запускаем uvicorn внутри .venv
python -m uvicorn apps.backend_core.main:app --host 127.0.0.1 --port 8181 --log-level info

REM 4. Возвращаем код возврата uvicorn обратно в NSSM
exit /b %ERRORLEVEL%
