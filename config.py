# Configuration file for AI Chat App

# Flask Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8888
FLASK_DEBUG = False  # Set to False for production
SECRET_KEY = "your-secret-key-here-change-in-production"

# Database Configuration
DATABASE_NAME = "chatapp.db"

# Ollama Configuration
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:1b-instruct-q4_K_M"
OLLAMA_TIMEOUT = 30

# Session Configuration
SESSION_LIFETIME_HOURS = 1

# UI Configuration
APP_NAME = "AI Chat App"
APP_TITLE = "🤖 AI Chat Assistant"
WELCOME_MESSAGE = "Hello! I'm your AI assistant. How can I help you today? 🚀"
