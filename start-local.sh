#!/bin/bash
# start-local.sh - Start Flask app locally

echo "🚀 Starting AI Chat App Locally..."
echo "=================================="

# Check if Docker is available for Ollama
if command -v docker &> /dev/null; then
    echo "🐳 Docker found. Checking Ollama container..."
    
    # Check if Ollama container is running
    if docker ps --format "table {{.Names}}" | grep -q "ollama-server"; then
        echo "✅ Ollama container is already running"
    else
        echo "🚀 Starting Ollama container..."
        docker-compose up -d ollama
        
        echo "⏳ Waiting for Ollama to be ready..."
        sleep 10
        
        # Check if model exists, if not pull it
        if ! docker exec ollama-server ollama list | grep -q "llama3.2:1b-instruct-q4_K_M"; then
            echo "📥 Pulling AI model (this may take a few minutes)..."
            docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M
        else
            echo "✅ AI model is already available"
        fi
    fi
    
    # Test Ollama connection
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        echo "✅ Ollama is responding"
    else
        echo "⚠️ Ollama might not be ready yet. AI features may not work initially."
    fi
else
    echo "⚠️ Docker not found. You'll need to install Ollama locally for AI features."
fi

echo ""
echo "🌐 Starting Flask development server..."
echo "======================================"
echo "📡 Server will be accessible at:"
echo "   - Local: http://127.0.0.1:8888"
echo "   - Network: http://10.0.0.4:8888"
echo "   - External: http://20.192.16.3:8888"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python3 app.py
