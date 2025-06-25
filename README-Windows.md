# 🚀 AI Chat App - Windows Setup Guide

This guide will help you run the AI Chat App on Windows.

## 📋 Prerequisites

### Required:
- **Python 3.8+** - Download from [python.org](https://python.org)
- **Git** (optional) - For cloning the repository

### For AI Features:
- **Docker Desktop** - Download from [docker.com](https://www.docker.com/products/docker-desktop)
- OR **Ollama for Windows** - Download from [ollama.ai](https://ollama.ai/download)

## 🎯 Quick Start

### Option 1: One-Click Setup (Recommended)
1. **Download** or clone this project
2. **Open Command Prompt** in the project folder
3. **Run setup**: Double-click `setup-local.bat`
4. **Start app**: Double-click `start-local.bat`
5. **Open browser**: Go to http://localhost:8888

### Option 2: Manual Setup
```cmd
# Install dependencies
pip install -r requirements.txt

# Setup Ollama (for AI features)
setup-ollama-windows.bat

# Start the app
python app.py
```

### Option 3: Virtual Environment (Best Practice)
```cmd
# Create and setup virtual environment
setup-venv-windows.bat

# Activate virtual environment
venv\Scripts\activate.bat

# Start the app
python app.py
```

## 🤖 AI Setup Options

### Docker (Recommended)
1. Install Docker Desktop
2. Run: `setup-ollama-windows.bat`
3. Wait for model download (may take 10-15 minutes)

### Local Ollama Installation
1. Download Ollama from [ollama.ai](https://ollama.ai/download)
2. Install and start Ollama
3. Open Command Prompt and run:
   ```cmd
   ollama pull llama3.2:1b-instruct-q4_K_M
   ```

## 🌐 Accessing the App

Once running, open your browser and go to:
- **Local**: http://localhost:8888
- **Network**: http://[your-ip]:8888

## 🔧 Troubleshooting

### Common Issues:

**"Python not found"**
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

**"Docker not found"**
- Install Docker Desktop
- Start Docker Desktop and wait for it to be ready

**"Port already in use"**
- Close other applications using port 8888
- Or change the port in `config.py`

**"Permission denied"**
- Run Command Prompt as Administrator
- Check Windows Firewall settings

**AI not responding**
- Make sure Docker Desktop is running
- Check if Ollama container is running: `docker ps`
- Restart Ollama: `docker-compose restart ollama`

### Useful Commands:
```cmd
# Check what's running on port 8888
netstat -an | findstr :8888

# Check Docker containers
docker ps

# Check Ollama models
docker exec ollama-server ollama list

# Restart Ollama
docker-compose restart ollama

# View app logs
python app.py
```

## 📁 Project Structure
```
GPT-llama/
├── app.py                     # Main Flask application
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker configuration
├── templates/                 # HTML templates
├── static/                    # CSS, JS, images
├── start-local.bat           # Windows startup script
├── setup-local.bat           # Windows setup script
├── setup-ollama-windows.bat  # Ollama setup script
└── setup-venv-windows.bat    # Virtual environment setup
```

## ⚙️ Configuration

Edit `config.py` to customize:
- **Port**: Change `FLASK_PORT = 8888` to your preferred port
- **Host**: Change `FLASK_HOST` for network access
- **AI Model**: Change `OLLAMA_MODEL` to use different models
- **Timeout**: Adjust `OLLAMA_TIMEOUT` for slower systems

## 🎨 Features

- ✅ User registration and login
- ✅ Real-time AI chat interface
- ✅ Chat history tracking
- ✅ User profile management
- ✅ Dark mode UI
- ✅ Responsive design
- ✅ Session management

## 🆘 Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Look at the console output for error messages
3. Check Windows Event Viewer for system-level issues
4. Make sure all prerequisites are installed and running

## 🚀 Deployment

For production deployment on Windows:
- Use IIS with Python CGI
- Or use a WSGI server like Waitress
- Set `FLASK_DEBUG = False` in config.py
- Use a proper database instead of SQLite
- Set up proper logging and monitoring

---

**Happy Chatting! 🤖💬**
