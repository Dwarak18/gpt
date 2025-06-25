@echo off
REM setup-venv-windows.bat - Setup Python virtual environment on Windows

echo 🐍 Setting up Python Virtual Environment on Windows...
echo ====================================================

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python not found. Please install Python from https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

echo ✅ Python found: %PYTHON_CMD%

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist "venv" (
    echo ⚠️ Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

%PYTHON_CMD% -m venv venv

if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created

REM Activate virtual environment and install dependencies
echo 🔧 Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✅ Dependencies installed successfully
    ) else (
        echo ⚠️ Some dependencies might have failed to install
    )
) else (
    echo ⚠️ requirements.txt not found. Installing basic dependencies...
    pip install flask werkzeug requests
)

echo.
echo 🎉 Virtual environment setup complete!
echo =====================================
echo 📋 To use the virtual environment:
echo    1. Activate: venv\Scripts\activate.bat
echo    2. Run app: python app.py
echo    3. Deactivate: deactivate
echo.
echo 🚀 Or use the start script: start-local.bat
echo.

pause
