@echo off
REM Quick launcher for Telegraf (after initial setup)
cd /d "%~dp0"

echo Starting Telegraf...
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run START.bat first to set up the project.
    echo.
    pause
    exit /b 1
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check if main.py exists
if not exist "client\main.py" (
    echo ERROR: client\main.py not found!
    echo.
    pause
    exit /b 1
)

REM Launch client
python client\main.py

REM Check for errors
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Application crashed with error code %errorlevel%
    echo Check logs\error.log for details
    echo.
    pause
)
