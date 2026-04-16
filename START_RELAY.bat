@echo off
REM Start local relay server for testing
cd /d "%~dp0"

echo Starting Telegraf Relay Server...
echo.
echo Server will run on ws://localhost:8765
echo.
echo Keep this window open while testing.
echo Press Ctrl+C to stop.
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run START.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Check if relay server exists
if not exist "relay\server.py" (
    echo ERROR: relay\server.py not found!
    pause
    exit /b 1
)

cd relay
python server.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Server crashed with error code %errorlevel%
    pause
)

cd ..
pause
