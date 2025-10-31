@echo off
cd /d C:\work\AICORPORATION\AIOFFICE
C:\work\AICORPORATION\AIOFFICE\.venv\Scripts\python.exe -m uvicorn apps.backend_core.main:app --host 127.0.0.1 --port 8100 --log-level info
