@echo off
REM setup-local.bat - Setup dependencies for local development on Windows

echo 📦 Setting up AI Chat App for Local Development on Windows...
echo ==========================================================

REM Check Python version
echo 🐍 Checking Python version...
python --version 2>nul
if %errorlevel% neq 0 (
    python3 --version 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Python not found. Please install Python from https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
    set PIP_CMD=pip3
) else (
    set PYTHON_CMD=python
    set PIP_CMD=pip
)

echo ✅ Python found: %PYTHON_CMD%

REM Install Python dependencies
echo 📋 Installing Python dependencies...
if exist "requirements.txt" (
    %PIP_CMD% install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✅ Python dependencies installed successfully
    ) else (
        echo ⚠️ Some dependencies might have failed to install
    )
) else (
    echo ⚠️ requirements.txt not found. Installing basic dependencies...
    %PIP_CMD% install flask werkzeug requests
)

echo.
echo 💡 Virtual Environment Setup (Recommended):
echo ==========================================
echo For better dependency management, consider using a virtual environment:
echo    %PYTHON_CMD% -m venv venv
echo    venv\Scripts\activate
echo    pip install -r requirements.txt
echo.

REM Check Docker for Ollama
echo 🐳 Checking Docker...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker found. You can use Docker for Ollama (recommended).
    echo    Run: docker-compose up -d ollama
    echo.
    
    REM Check if docker-compose.yml exists
    if exist "docker-compose.yml" (
        echo ✅ docker-compose.yml found
        echo 🚀 You can start Ollama with: docker-compose up -d ollama
    ) else (
        echo ⚠️ docker-compose.yml not found in current directory
    )
) else (
    echo ❌ Docker not found. Please install one of the following:
    echo    - Docker Desktop: https://www.docker.com/products/docker-desktop
    echo    - Ollama for Windows: https://ollama.ai/download
)

echo.
echo 🎉 Setup complete! 
echo ==================
echo 📋 Next steps:
echo    1. Double-click 'start-local.bat' to run the app
echo    2. Or run manually: %PYTHON_CMD% app.py
echo    3. Open your browser to: http://localhost:8888
echo.
echo 🔧 If you have issues:
echo    - Make sure Docker Desktop is running (for AI features)
echo    - Check Windows Firewall settings
echo    - Try running as Administrator if needed
echo.

pause
