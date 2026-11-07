@echo off
title SENTINEL AI - Launcher
echo.
echo  =====================================================
echo   SENTINEL AI -- Full System Launcher
echo   AI-Powered Fake Review Detection System
echo  =====================================================
echo.
echo  This will open TWO windows:
echo    1. Backend API Server  --  http://127.0.0.1:8000
echo    2. Frontend UI         --  http://localhost:3000
echo.
echo  After both windows say "ready" or "Application startup complete",
echo  open your browser at:  http://localhost:3000
echo.
pause

echo Launching Backend Server...
start "Sentinel AI - Backend" cmd /k "cd /d D:\firstproject\backend && call venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo Launching Frontend Server...
start "Sentinel AI - Frontend" cmd /k "cd /d D:\firstproject\frontend && npm run dev"

echo.
echo  =====================================================
echo   Both servers are starting in separate windows.
echo.
echo   Wait until you see these messages:
echo     Backend : "Application startup complete."
echo     Frontend: "ready in ... ms"
echo.
echo   Then open:  http://localhost:3000
echo  =====================================================
echo.
pause
