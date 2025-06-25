@echo off
echo.
echo ========================================
echo        AI Chat App with Flask
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✓ Python is installed

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [3/4] Checking Ollama connection...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama is not running or not accessible
    echo Please make sure:
    echo - Ollama is installed from https://ollama.com
    echo - Ollama service is running
    echo - Model llama3.2:1b-instruct-q4_K_M is downloaded
    echo.
    echo To download the model, run: ollama pull llama3.2:1b-instruct-q4_K_M
    echo.
    echo The app will start but AI features won't work without Ollama
    pause
) else (
    echo ✓ Ollama is running
)

echo.
echo [4/4] Starting the application...
echo.
echo ========================================
echo   App will be available at:
echo   http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py
