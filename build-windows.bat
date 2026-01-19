@echo off
echo ========================================
echo Immich Uploader - Build Standalone EXE
echo ========================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from: https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo Building executable...
echo This may take a few minutes...
echo.

REM Build the executable
pyinstaller --onefile --windowed --name "ImmichUploader" --icon=icon.ico immich_uploader.py

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your executable is ready:
echo   dist\ImmichUploader.exe
echo.
echo This is a STANDALONE file - no dependencies needed!
echo Just copy ImmichUploader.exe to any Windows computer and run it.
echo.
pause
