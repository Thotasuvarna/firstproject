@echo off
title Sentinel AI - Seed Database
echo ========================================================
echo Seeding Sentinel AI database with demo data...
echo ========================================================
cd backend
call .\venv\Scripts\activate.bat
python seed_data.py
pause
