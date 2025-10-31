@echo off
cd /d C:\work\AICORPORATION\AIOFFICE
call .\.venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
