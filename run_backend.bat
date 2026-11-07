@echo off
title Sentinel AI - FastAPI Backend Server
echo ========================================================
echo   SENTINEL AI -- Backend API Server (FastAPI)
echo   URL: http://127.0.0.1:8000
echo   API Docs: http://127.0.0.1:8000/docs
echo ========================================================
echo.

cd /d "D:\firstproject\backend"

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found at D:\firstproject\backend\venv
    echo Please contact support.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Starting server... Please wait...
echo.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
