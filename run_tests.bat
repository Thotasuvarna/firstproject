@echo off
title Sentinel AI - Run Automated Tests
echo ========================================================
echo Executing Backend & AI Test Suite with Pytest...
echo ========================================================
cd backend
call .\venv\Scripts\activate.bat
python -m pytest tests/test_backend.py -v -o norecursedirs=venv
pause
