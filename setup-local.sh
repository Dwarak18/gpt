#!/bin/bash
# setup-local.sh - Setup dependencies for local development

echo "📦 Setting up AI Chat App for Local Development..."
echo "================================================"

# Check Python version
echo "🐍 Checking Python version..."
python3 --version

# Install Python dependencies
echo "📋 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "⚠️ requirements.txt not found. Installing basic dependencies..."
    pip3 install flask werkzeug requests
fi

# Check if virtual environment is preferred
echo ""
echo "💡 Tip: For better dependency management, consider using a virtual environment:"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo ""

# Check Docker for Ollama
if command -v docker &> /dev/null; then
    echo "🐳 Docker found. You can use Docker for Ollama (recommended)."
    echo "   Run: docker-compose up -d ollama"
else
    echo "📥 Docker not found. Install Docker or Ollama locally:"
    echo "   - Docker: https://docs.docker.com/get-docker/"
    echo "   - Ollama: https://ollama.ai/download"
fi

echo ""
echo "🎉 Setup complete! Run the app with:"
echo "   chmod +x start-local.sh"
echo "   ./start-local.sh"
echo ""
echo "Or manually:"
echo "   python3 app.py"
