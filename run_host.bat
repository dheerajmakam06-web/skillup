@echo off
cd /d "%~dp0"
set HOST=0.0.0.0
if "%PORT%"=="" set PORT=5000
python app.py
pause
