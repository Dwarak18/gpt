# 🤖 AI Chat App with Flask & Ollama

A beautiful and modern AI chat application built with Flask, featuring user authentication, real-time chat with AI using Ollama (Llama 3.2), and a responsive design.

## ✨ Features

- 🔐 **User Authentication**: Secure login and signup with password hashing
- 💬 **AI Chat Interface**: Real-time chat with Ollama AI model (Llama 3.2)
- 👤 **User Profiles**: Personal profile management
- 📱 **Responsive Design**: Beautiful UI that works on all devices
- 🎨 **Modern UI**: Gradient backgrounds, glassmorphism effects, and smooth animations
- 📊 **Chat History**: Track your conversations with the AI
- 🔄 **Connection Status**: Real-time AI service status monitoring
- � **Docker Integration**: Easy Ollama setup with Docker

## 🛠️ Prerequisites

- **Python 3.8+** installed
- **Docker Desktop** installed and running
- **Git** (optional, for cloning)

## 🚀 Quick Setup & Run

### Method 1: Windows Batch Scripts (Easiest)

1. **Download/Clone the project**
   ```bash
   git clone <your-repository-url>
   cd GPT-llama
   ```

2. **One-click setup (Windows)**
   ```batch
   # Run the complete setup script
   setup-local.bat
   ```
   This script will:
   - Check Docker installation
   - Start Ollama container with Docker
   - Download Llama 3.2 model
   - Create Python virtual environment
   - Install all dependencies

3. **Start the application**
   ```batch
   start-local.bat
   ```
   This will start both Ollama and the Flask app.

### Method 2: Manual Setup (All Platforms)

#### Step 1: Setup Ollama with Docker

1. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Verify Docker is running: `docker --version`

2. **Start Ollama Container**
   ```bash
   # Using Docker Compose (recommended)
   docker-compose up -d
   
   # Or manually
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama-server ollama/ollama:latest
   ```

3. **Download the AI Model**
   ```bash
   # Download Llama 3.2 model (this may take a few minutes)
   docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M
   ```

4. **Verify Ollama is working**
   ```bash
   # Check if container is running
   docker ps
   
   # Check available models
   docker exec ollama-server ollama list
   ```

#### Step 2: Setup Python Environment

1. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/Mac
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

#### Step 3: Run the Application

1. **Start the Flask App**
   ```bash
   python app.py
   ```

2. **Access the Application**
   - Open your browser and go to: **http://localhost:8888**
   - You should see the AI Chat App login page

## 🎯 Usage Instructions

### First Time Setup
1. **Create Account**: Click "Sign Up" and create a new account
2. **Login**: Use your credentials to login
3. **Start Chatting**: Begin your conversation with the AI assistant!

### Using the Chat Interface
- **Send Messages**: Type your message and press Enter or click the send button
- **AI Responses**: The AI will respond using the Llama 3.2 model
- **Connection Status**: Green indicator shows AI is connected and ready
- **Profile**: Click on your username to view/edit your profile
- **Logout**: Use the dropdown menu to logout

## � Configuration

The app uses `config.py` for configuration. Key settings:

```python
# Flask Configuration
FLASK_HOST = "0.0.0.0"        # Host to bind to
FLASK_PORT = 8888             # Port to run on
FLASK_DEBUG = True            # Debug mode

# Ollama Configuration
OLLAMA_URL = "http://localhost:11434"           # Ollama API URL
OLLAMA_MODEL = "llama3.2:1b-instruct-q4_K_M"   # AI Model
OLLAMA_TIMEOUT = 30                             # Request timeout

# Database
DATABASE_NAME = "chatapp.db"  # SQLite database file
```

## 📁 Project Structure

```
GPT-llama/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker setup for Ollama
├── chatapp.db               # SQLite database (auto-created)
├── .venv/                   # Python virtual environment
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── signup.html         # Registration page
│   ├── chat.html           # Main chat interface
│   └── profile.html        # User profile page
├── setup-local.bat         # Windows setup script
├── start-local.bat         # Windows start script
├── setup-local.sh          # Linux setup script
├── start-local.sh          # Linux start script
└── README.md               # This file
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Unable to connect to AI service"
**Cause**: Ollama container not running or model not loaded
**Solutions**:
```bash
# Check if Ollama container is running
docker ps

# Restart Ollama container
docker restart ollama-server

# Check Ollama logs
docker logs ollama-server

# Verify model is available
docker exec ollama-server ollama list
```

#### 2. "Port already in use" 
**Cause**: Another app is using port 8888 or 11434
**Solutions**:
```bash
# For Flask app (change port in config.py)
FLASK_PORT = 8889  # Or any other available port

# For Ollama (change docker-compose.yml)
ports:
  - "11435:11434"  # Change external port
```

#### 3. "Python module not found"
**Cause**: Virtual environment not activated or dependencies not installed
**Solutions**:
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

#### 4. Docker issues
**Cause**: Docker not running or permission issues
**Solutions**:
```bash
# Start Docker Desktop
# Or restart Docker service on Linux
sudo systemctl restart docker

# Check Docker status
docker --version
docker info
```

### Testing the Setup

#### Test Ollama Connection
```bash
# Test Ollama API
curl http://localhost:11434/api/tags

# Test AI response
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b-instruct-q4_K_M",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

#### Test Flask App
```bash
# Check if Flask is running
curl http://localhost:8888

# Or open in browser
http://localhost:8888
```

## 🚀 Deployment Options

### Local Development (Default)
The app runs in debug mode with auto-reload enabled:
```bash
python app.py
# Access at: http://localhost:8888
```

### Production Deployment with Apache

1. **Install Apache and mod_wsgi**
   ```bash
   # Ubuntu/Debian
   sudo apt install apache2 libapache2-mod-wsgi-py3
   
   # CentOS/RHEL
   sudo yum install httpd python3-mod_wsgi
   ```

2. **Use provided Apache configuration**
   ```bash
   # Copy Apache config
   sudo cp apache-flaskapp.conf /etc/apache2/sites-available/
   sudo a2ensite apache-flaskapp
   sudo systemctl reload apache2
   ```

3. **Set proper permissions**
   ```bash
   # Run the provided permission script
   chmod +x fix-permissions.sh
   ./fix-permissions.sh
   ```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8888 app:app
```

## 🎨 Customization

### Changing the AI Model
1. **Download a different model**:
   ```bash
   docker exec ollama-server ollama pull llama3.2:3b-instruct-q4_K_M
   ```

2. **Update config.py**:
   ```python
   OLLAMA_MODEL = "llama3.2:3b-instruct-q4_K_M"
   ```

### Modifying the UI
- **Colors & Themes**: Edit CSS variables in `templates/base.html`
- **Layout**: Modify individual template files
- **Styling**: Add custom CSS classes and animations

### Adding Features
- **Chat History Export**: Add download functionality
- **File Uploads**: Extend for document analysis
- **Multiple Models**: Support model switching
- **User Roles**: Add admin functionality

## 🔧 Development Tips

### Running in Development Mode
```bash
# Enable debug mode
export FLASK_DEBUG=True  # Linux/Mac
set FLASK_DEBUG=True     # Windows

# Auto-reload on changes
python app.py
```

### Database Management
```bash
# Reset database
rm chatapp.db
python app.py  # Will recreate automatically

# View database content
sqlite3 chatapp.db
.tables
SELECT * FROM users;
```

### Docker Commands Reference
```bash
# Start Ollama container
docker-compose up -d

# Stop Ollama container
docker-compose down

# View logs
docker logs ollama-server

# Enter container
docker exec -it ollama-server /bin/bash

# Download models
docker exec ollama-server ollama pull <model-name>

# List models
docker exec ollama-server ollama list
```

## 📊 Performance Notes

- **Model Size**: llama3.2:1b-instruct-q4_K_M is ~800MB (optimized for speed)
- **Memory Usage**: Typically uses 1-2GB RAM when active
- **Response Time**: Usually 1-5 seconds depending on system specs
- **Concurrent Users**: Flask dev server handles ~10 concurrent users

## 🔐 Security Considerations

### For Production Use:
1. **Change Secret Key**: Update `SECRET_KEY` in config.py
2. **Use HTTPS**: Configure SSL/TLS certificates
3. **Database Security**: Use PostgreSQL/MySQL with proper credentials
4. **Environment Variables**: Store sensitive config in environment variables
5. **Firewall Rules**: Restrict access to necessary ports only

### Example Production Config:
```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-very-secure-key')
FLASK_DEBUG = False
DATABASE_NAME = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/chatapp')
```

## 📞 Support & FAQ

### Frequently Asked Questions

**Q: Can I use a different AI model?**
A: Yes! Download any Ollama-compatible model and update the `OLLAMA_MODEL` setting.

**Q: Can I deploy this to cloud services?**
A: Yes! It works on AWS, Azure, Google Cloud, Heroku, etc. You'll need to modify the Docker setup for cloud deployment.

**Q: Is this suitable for production?**
A: The code is production-ready, but you should implement proper security measures, use a production database, and configure proper hosting.

**Q: How do I backup my data?**
A: Copy the `chatapp.db` file. For production, set up regular database backups.

### Getting Help
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check Docker and Ollama logs for errors
4. Ensure all ports are available (8888, 11434)

## � License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for the excellent AI model serving
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Llama 3.2](https://llama.meta.com/) for the AI model
- The open-source community for inspiration and tools

---

**Ready to chat with AI? Get started now! 🚀🤖**

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
