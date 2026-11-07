@echo off
title Sentinel AI - React Frontend
echo ========================================================
echo   SENTINEL AI -- React Frontend (Vite Dev Server)
echo   URL: http://localhost:3000
echo ========================================================
echo.

cd /d "D:\firstproject\frontend"

if not exist "package.json" (
    echo ERROR: Could not find frontend\package.json
    echo Make sure D:\firstproject\frontend exists.
    pause
    exit /b 1
)

echo Starting frontend on http://localhost:3000 ...
echo.
npm run dev
pause
