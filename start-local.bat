@echo off
REM start-local.bat - Start Flask app locally on Windows

echo 🚀 Starting AI Chat App Locally on Windows...
echo =============================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Trying python3...
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python not found. Please install Python first.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

echo ✅ Python found: %PYTHON_CMD%

REM Check if Docker is available for Ollama
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 🐳 Docker found. Checking Ollama container...
    
    REM Check if Ollama container is running
    docker ps --format "table {{.Names}}" | findstr "ollama-server" >nul
    if %errorlevel% neq 0 (
        echo 🚀 Starting Ollama container...
        docker-compose up -d ollama
        
        echo ⏳ Waiting for Ollama to be ready...
        timeout /t 10 /nobreak >nul
        
        REM Pull AI model if not exists
        echo 📥 Pulling AI model (this may take a few minutes)...
        docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M
    ) else (
        echo ✅ Ollama container is already running
    )
    
    REM Test Ollama connection
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Ollama is responding
    ) else (
        echo ⚠️ Ollama might not be ready yet. AI features may not work initially.
    )
) else (
    echo ⚠️ Docker not found. You'll need to install Docker Desktop or Ollama locally for AI features.
    echo 📥 Download Docker Desktop: https://www.docker.com/products/docker-desktop
    echo 📥 Or download Ollama: https://ollama.ai/download
)

echo.
echo 🌐 Starting Flask development server...
echo ====================================
echo 📡 Server will be accessible at:
echo    - Local: http://127.0.0.1:8888
echo    - Network: http://localhost:8888
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask app
%PYTHON_CMD% app.py

pause
