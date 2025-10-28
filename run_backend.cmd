@echo off
cd /d C:\work\AICORPORATION\AIOFFICE
C:\work\AICORPORATION\AIOFFICE\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 >> C:\work\AICORPORATION\AIOFFICE\logs\backend_service.log 2>&1
