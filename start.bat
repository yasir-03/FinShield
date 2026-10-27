@echo off
title FinShield
cd /d "%~dp0"

echo ========================================
echo          Starting FinShield
echo ========================================
echo.

if not exist "%~dp0venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found.
    echo Please check that the venv folder exists.
    pause
    exit /b 1
)

"%~dp0venv\Scripts\python.exe" "%~dp0app.py"

echo.
echo FinShield has stopped.
pause