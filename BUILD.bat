@echo off
REM Build Telegraf.exe
cd /d "%~dp0"

echo Building Telegraf.exe...
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run START.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Check if build script exists
if not exist "scripts\build.py" (
    echo ERROR: scripts\build.py not found!
    pause
    exit /b 1
)

python scripts\build.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed with error code %errorlevel%
    pause
    exit /b 1
)

echo.
echo Build complete! Check dist\Telegraf.exe
pause
