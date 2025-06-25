@echo off
REM setup-ollama-windows.bat - Setup Ollama on Windows

echo 🤖 Setting up Ollama on Windows...
echo =================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found. Please install Docker Desktop first.
    echo 📥 Download from: https://www.docker.com/products/docker-desktop
    echo.
    echo After installing Docker Desktop:
    echo 1. Start Docker Desktop
    echo 2. Wait for it to be ready
    echo 3. Run this script again
    pause
    exit /b 1
)

echo ✅ Docker found

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    echo 💡 Look for Docker Desktop in your system tray and make sure it's running.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Start Ollama container
echo 🚀 Starting Ollama container...
docker-compose up -d ollama

if %errorlevel% neq 0 (
    echo ❌ Failed to start Ollama container.
    echo 🔧 Try these troubleshooting steps:
    echo    1. Make sure docker-compose.yml exists in current directory
    echo    2. Check if port 11434 is available
    echo    3. Restart Docker Desktop
    pause
    exit /b 1
)

echo ✅ Ollama container started

REM Wait for Ollama to be ready
echo ⏳ Waiting for Ollama to be ready...
set /a attempts=0
:check_ollama
set /a attempts+=1
if %attempts% gtr 30 (
    echo ❌ Ollama took too long to start. Check container logs:
    echo    docker-compose logs ollama
    pause
    exit /b 1
)

curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Waiting for Ollama... (attempt %attempts%/30)
    timeout /t 2 /nobreak >nul
    goto check_ollama
)

echo ✅ Ollama is ready!

REM Pull the AI model
echo 📥 Pulling llama3.2:1b-instruct-q4_K_M model...
echo ⚠️ This may take several minutes depending on your internet connection...
docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M

if %errorlevel% equ 0 (
    echo ✅ Model downloaded successfully!
) else (
    echo ⚠️ Model download may have failed. You can try again later with:
    echo    docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M
)

REM Test the setup
echo 🧪 Testing Ollama setup...
curl -s -X POST http://localhost:11434/api/generate ^
    -H "Content-Type: application/json" ^
    -d "{\"model\": \"llama3.2:1b-instruct-q4_K_M\", \"prompt\": \"Hello\", \"stream\": false}" > test_response.json

findstr "response" test_response.json >nul
if %errorlevel% equ 0 (
    echo ✅ Ollama test successful!
    del test_response.json >nul 2>&1
) else (
    echo ⚠️ Ollama test failed. Check test_response.json for details.
)

echo.
echo 🎉 Ollama setup complete!
echo ========================
echo 📋 Summary:
echo    - Ollama running at: http://localhost:11434
echo    - Model: llama3.2:1b-instruct-q4_K_M
echo    - Container: ollama-server
echo.
echo 🚀 You can now run your Flask app with: start-local.bat
echo 🔍 To check container status: docker ps
echo 🛑 To stop Ollama: docker-compose down
echo.

pause
