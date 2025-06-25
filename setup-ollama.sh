#!/bin/bash
# setup-ollama.sh - Setup script for Ollama with llama3.2 model

echo "🐳 Setting up Ollama with Docker..."
echo "================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start Ollama container
echo "🚀 Starting Ollama container..."
docker-compose up -d ollama

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
sleep 10

# Check if Ollama is responding
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    else
        echo "⏳ Waiting for Ollama... (attempt $((attempt + 1))/$max_attempts)"
        sleep 5
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Ollama failed to start within the expected time."
    echo "📋 Check container logs: docker-compose logs ollama"
    exit 1
fi

# Pull the llama3.2 model
echo "📥 Pulling llama3.2:1b-instruct-q4_K_M model..."
docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M

# Verify the model is available
echo "🔍 Verifying model installation..."
if docker exec ollama-server ollama list | grep -q "llama3.2:1b-instruct-q4_K_M"; then
    echo "✅ Model llama3.2:1b-instruct-q4_K_M is ready!"
else
    echo "❌ Model installation failed."
    exit 1
fi

# Test the API
echo "🧪 Testing Ollama API..."
response=$(curl -s -X POST http://localhost:11434/api/generate \
    -H "Content-Type: application/json" \
    -d '{
        "model": "llama3.2:1b-instruct-q4_K_M",
        "prompt": "Hello, can you hear me?",
        "stream": false
    }')

if echo "$response" | grep -q "response"; then
    echo "✅ Ollama API test successful!"
    echo "🎉 Setup complete! Ollama is ready to use."
    echo ""
    echo "📋 Summary:"
    echo "   - Ollama running at: http://localhost:11434"
    echo "   - Model: llama3.2:1b-instruct-q4_K_M"
    echo "   - Docker container: ollama-server"
    echo ""
    echo "🚀 You can now start your Flask app!"
else
    echo "❌ API test failed. Response:"
    echo "$response"
fi
