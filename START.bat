@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Telegraf - Automated Setup and Launch
color 0A

echo.
echo ═══════════════════════════════════════════════════════
echo    TELEGRAF - Automated Messenger Setup
echo ═══════════════════════════════════════════════════════
echo.

REM Check if Python is installed
echo [1/8] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python 3.11...

    REM Download Python installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe' -OutFile 'python_installer.exe'}"

    REM Install Python silently
    echo Installing Python (this may take a few minutes)...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    REM Wait for installation
    timeout /t 30 /nobreak >nul

    REM Clean up
    del python_installer.exe

    echo Python installed successfully!
    echo Please restart this script after Python installation.
    pause
    exit /b 0
) else (
    echo Python is already installed.
)

echo.
echo [2/8] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo [3/8] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [4/8] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo.
echo [5/8] Installing dependencies...
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    pause
    exit /b 1
)

pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo Error installing dependencies. Trying again with verbose output...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo [6/8] Creating project directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "dist" mkdir dist
echo Directories created.

echo.
echo [7/8] Building executable...
if exist "scripts\build.py" (
    python scripts\build.py
    if %errorlevel% neq 0 (
        echo Warning: Build failed. You can still run from source.
    )
) else (
    echo Warning: build.py not found. Skipping build step.
)

echo.
echo [8/8] Launching Telegraf...
echo.
echo ═══════════════════════════════════════════════════════
echo    Setup Complete!
echo ═══════════════════════════════════════════════════════
echo.
echo Starting Telegraf client...
echo.

REM Check if relay server is configured
echo NOTE: Make sure to configure relay server in config\config.json
echo Default: ws://localhost:8765
echo.
echo For global connectivity, deploy relay server to:
echo   - Render.com
echo   - Railway.app
echo   - Fly.io
echo.
echo See relay\README.md for deployment instructions.
echo.

timeout /t 3 /nobreak >nul

REM Check if main.py exists
if not exist "client\main.py" (
    echo ERROR: client\main.py not found!
    pause
    exit /b 1
)

REM Launch client
python client\main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application crashed with error code %errorlevel%
    echo Check logs\error.log for details
    pause
)
