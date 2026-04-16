@echo off
cd /d "%~dp0"

echo ========================================
echo   TELEGRAF INSTALLER BUILDER
echo ========================================
echo.

REM Check if Inno Setup is installed
set "INNO_PATH=D:\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)
if not exist "%INNO_PATH%" (
    echo ERROR: Inno Setup not found!
    echo.
    echo Please install Inno Setup 6 from:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo Checked paths:
    echo   D:\Inno Setup 6\ISCC.exe
    echo   C:\Program Files (x86)\Inno Setup 6\ISCC.exe
    echo.
    pause
    exit /b 1
)

REM Check if dist\Telegraf.exe exists
if not exist "dist\Telegraf.exe" (
    echo ERROR: Telegraf.exe not found in dist folder!
    echo.
    echo Please build the application first:
    echo   BUILD.bat
    echo.
    pause
    exit /b 1
)

REM Check if installer script exists
if not exist "installer\telegraf.iss" (
    echo ERROR: Installer script not found!
    echo Expected: installer\telegraf.iss
    echo.
    pause
    exit /b 1
)

REM Create installer directory if it doesn't exist
if not exist "installer" mkdir installer

echo [1/3] Validating files...
echo   - Inno Setup: Found
echo   - Telegraf.exe: Found
echo   - Installer script: Found
echo.

echo [2/3] Building installer...
echo.
"%INNO_PATH%" "installer\telegraf.iss"

if errorlevel 1 (
    echo.
    echo ERROR: Installer build failed!
    echo Check the output above for details.
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Verifying output...

if exist "installer\Telegraf_Setup.exe" (
    echo.
    echo ========================================
    echo   SUCCESS! Installer created!
    echo ========================================
    echo.
    echo Location: installer\Telegraf_Setup.exe
    echo.
    echo You can now:
    echo   1. Test: Run installer\Telegraf_Setup.exe
    echo   2. Share: Send the installer to users
    echo   3. Distribute: Upload to your website
    echo.
) else (
    echo.
    echo ERROR: Installer file not created!
    echo Expected: installer\Telegraf_Setup.exe
    echo.
    pause
    exit /b 1
)

pause
