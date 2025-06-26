dod# 🤖 AI Chat App with Flask & Ollama

A beautiful and modern AI chat application built with Flask, featuring user authentication, real-time chat with AI using Ollama (Llama 3.2), and a responsive design.

## ✨ Features

- 🔐 **User Authentication**: Secure login and signup with password hashing
- 💬 **AI Chat Interface**: Real-time chat with Ollama AI model (Llama 3.2)
- 👤 **User Profiles**: Personal profile management
- � **Multiple Chat Sessions**: Create and manage separate chat conversations
- �📱 **Responsive Design**: Beautiful UI that works on all devices
- 🎨 **Modern UI**: Gradient backgrounds, glassmorphism effects, and smooth animations
- 📊 **Chat History**: Persistent chat history - see previous conversations when you log in
- 🔄 **Connection Status**: Real-time AI service status monitoring
- � **Docker Integration**: Easy Ollama setup with Docker

## 🛠️ Prerequisites

- **Python 3.8+** installed
- **Docker Desktop** installed and running
- **Git** (optional, for cloning)

## 🚀 Quick Setup & Run

### Method 1: Automated Setup Scripts

#### Windows (Easiest)

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

#### Linux/macOS (One-command setup)

1. **Download/Clone the project**
   ```bash
   git clone <your-repository-url>
   cd GPT-llama
   ```

2. **One-click setup (Linux/macOS)**
   ```bash
   # Make script executable and run
   chmod +x setup-local.sh
   ./setup-local.sh
   ```
   This script will:
   - Check Docker installation
   - Start Ollama container with Docker
   - Download Llama 3.2 model
   - Create Python virtual environment
   - Install all dependencies

3. **Start the application**
   ```bash
   chmod +x start-local.sh
   ./start-local.sh
   ```
   This will start both Ollama and the Flask app.

### Method 2: Manual Setup (All Platforms)

#### Step 1: Install Prerequisites

##### Windows
1. **Install Python 3.8+**
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: `python --version`

2. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Verify: `docker --version`

##### Linux (Ubuntu/Debian)
1. **Install Python 3.8+**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   python3 --version
   ```

2. **Install Docker**
   ```bash
   # Add Docker's official GPG key
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
     $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update

   # Install Docker packages
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

   # Add your user to docker group (logout/login required)
   sudo usermod -aG docker $USER
   newgrp docker

   # Verify installation
   docker --version
   docker compose version
   ```

3. **Install Git**
   ```bash
   sudo apt install git
   ```

##### Linux (CentOS/RHEL/Fedora)
1. **Install Python 3.8+**
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   
   # Fedora
   sudo dnf install python3 python3-pip python3-venv
   
   python3 --version
   ```

2. **Install Docker**
   ```bash
   # CentOS/RHEL
   sudo yum install -y yum-utils
   sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   
   # Fedora
   sudo dnf -y install dnf-plugins-core
   sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
   sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

   # Start and enable Docker
   sudo systemctl start docker
   sudo systemctl enable docker
   
   # Add user to docker group
   sudo usermod -aG docker $USER
   newgrp docker
   ```

##### macOS
1. **Install Python 3.8+**
   ```bash
   # Using Homebrew (recommended)
   brew install python3
   
   # Or download from https://www.python.org/downloads/
   python3 --version
   ```

2. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop
   - Install Docker Desktop for Mac
   - Verify: `docker --version`

#### Step 2: Setup Ollama with Docker

#### Step 3: Setup Ollama with Docker

1. **Clone/Download the project**
   ```bash
   git clone https://github.com/Dwarak18/gpt.git
   cd gpt
   ```

2. **Start Ollama Container**
   ```bash
   # Using Docker Compose (recommended)
   docker compose up -d
   
   # Or manually (all platforms)
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

#### Step 4: Setup Python Environment

##### Windows
```batch
# Create Virtual Environment
python -m venv .venv

# Activate Virtual Environment
.venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
```

##### Linux/macOS
```bash
# Create Virtual Environment
python3 -m venv .venv

# Activate Virtual Environment
source .venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

#### Step 5: Run the Application

##### All Platforms
```bash
# Make sure virtual environment is activated
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Start the Flask App
python app.py
```

**Access the Application:**
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
- **Multiple Chats**: Use the sidebar to manage multiple chat sessions
- **New Chat**: Click "New Chat" in the sidebar to start a fresh conversation
- **Switch Chats**: Click on any session in the sidebar to switch between conversations
- **Chat History**: Previous conversations are automatically loaded when you log in
- **Delete Chats**: Use the trash icon on each session to delete unwanted conversations
- **Clear History**: Use the dropdown menu to clear the current chat's history
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
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
```

#### 4. Docker issues
**Cause**: Docker not running or permission issues
**Solutions**:
```bash
# Windows: Start Docker Desktop from Start Menu

# Linux: Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Check Docker status
docker --version
docker info

# Fix permission issues (Linux)
sudo usermod -aG docker $USER
newgrp docker  # Or logout/login
```

#### 5. Permission denied (Linux)
**Cause**: User not in docker group or file permissions
**Solutions**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Fix file permissions
chmod +x setup-local.sh
chmod +x start-local.sh

# Or run with sudo (not recommended)
sudo docker ps
```

### Testing the Setup

#### Test Ollama Connection
```bash
# Test Ollama API (all platforms)
curl http://localhost:11434/api/tags

# Test AI response (all platforms)
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b-instruct-q4_K_M",
  "prompt": "Hello, how are you?",
  "stream": false
}'

# Windows alternative (if curl not available)
# Use PowerShell:
Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get
```

#### Test Flask App
```bash
# Check if Flask is running (all platforms)
curl http://localhost:8888

# Windows PowerShell alternative
Invoke-RestMethod -Uri "http://localhost:8888" -Method Get

# Or open in browser
http://localhost:8888
```

### Linux-Specific Troubleshooting

#### Docker daemon not running
```bash
# Check Docker service status
sudo systemctl status docker

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker
```

#### Firewall blocking ports
```bash
# Ubuntu/Debian - allow ports through UFW
sudo ufw allow 8888
sudo ufw allow 11434

# CentOS/RHEL - allow ports through firewalld
sudo firewall-cmd --permanent --add-port=8888/tcp
sudo firewall-cmd --permanent --add-port=11434/tcp
sudo firewall-cmd --reload
```

#### SELinux issues (CentOS/RHEL)
```bash
# Check SELinux status
sestatus

# Temporarily disable SELinux (if needed)
sudo setenforce 0

# Permanently disable (edit /etc/selinux/config)
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
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

#### Windows
```batch
# Enable debug mode
set FLASK_DEBUG=True

# Auto-reload on changes
python app.py
```

#### Linux/macOS
```bash
# Enable debug mode
export FLASK_DEBUG=True

# Auto-reload on changes
python app.py
```

### Database Management

#### Windows
```batch
# Reset database
del chatapp.db
python app.py  # Will recreate automatically

# View database content (if sqlite3 installed)
sqlite3 chatapp.db
.tables
SELECT * FROM users;
.quit
```

#### Linux/macOS
```bash
# Reset database
rm chatapp.db
python app.py  # Will recreate automatically

# View database content
sqlite3 chatapp.db
.tables
SELECT * FROM users;
.quit
```

### Docker Commands Reference

#### All Platforms
```bash
# Start Ollama container
docker compose up -d

# Stop Ollama container
docker compose down

# View logs
docker logs ollama-server

# Enter container
docker exec -it ollama-server /bin/bash

# Download models
docker exec ollama-server ollama pull <model-name>

# List models
docker exec ollama-server ollama list

# Remove container and volumes (clean reset)
docker compose down -v
docker volume rm ollama

# Check container resource usage
docker stats ollama-server
```

#### Linux-Specific Docker Commands
```bash
# Check Docker service status
sudo systemctl status docker

# Start/Stop/Restart Docker service
sudo systemctl start docker
sudo systemctl stop docker
sudo systemctl restart docker

# View Docker logs
sudo journalctl -u docker.service

# Clean up unused Docker resources
docker system prune -a
docker volume prune
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

## � Complete Linux Setup Guide

### Ubuntu/Debian (20.04+)

#### 1. System Update
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Prerequisites
```bash
# Install Python 3.8+, pip, and venv
sudo apt install python3 python3-pip python3-venv git curl -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (requires logout/login)
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt install docker-compose-plugin -y
```

#### 3. Setup the Project
```bash
# Clone the repository
git clone <your-repository-url>
cd GPT-llama

# Run the automated setup script
chmod +x setup-local.sh
./setup-local.sh

# Start the application
chmod +x start-local.sh
./start-local.sh
```

### CentOS/RHEL/Rocky Linux (8+)

#### 1. System Update
```bash
sudo dnf update -y
```

#### 2. Install Prerequisites
```bash
# Install Python 3.8+
sudo dnf install python3 python3-pip git curl -y

# Install Docker
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. Setup the Project
```bash
# Clone the repository
git clone <your-repository-url>
cd GPT-llama

# Run the automated setup script
chmod +x setup-local.sh
./setup-local.sh

# Start the application
chmod +x start-local.sh
./start-local.sh
```

### Arch Linux

#### 1. System Update
```bash
sudo pacman -Syu
```

#### 2. Install Prerequisites
```bash
# Install Python, Docker, and other tools
sudo pacman -S python python-pip git curl docker docker-compose

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. Setup the Project
```bash
# Clone the repository
git clone <your-repository-url>
cd GPT-llama

# Run the automated setup script
chmod +x setup-local.sh
./setup-local.sh

# Start the application
chmod +x start-local.sh
./start-local.sh
```

### Manual Linux Setup (Any Distribution)

If the automated scripts don't work, here's the manual process:

#### 1. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Start Ollama with Docker
```bash
# Start Ollama container
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama-server ollama/ollama:latest

# Wait for container to start, then download model
sleep 10
docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M
```

#### 4. Start the Flask Application
```bash
python app.py
```

#### 5. Access the Application
Open your browser and navigate to: `http://localhost:8888`

### Linux Service Setup (Optional)

To run the app as a systemd service:

#### 1. Create Service File
```bash
sudo nano /etc/systemd/system/ai-chat-app.service
```

#### 2. Add Service Configuration
```ini
[Unit]
Description=AI Chat App
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/GPT-llama
Environment=PATH=/path/to/GPT-llama/.venv/bin
ExecStart=/path/to/GPT-llama/.venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-chat-app.service
sudo systemctl start ai-chat-app.service
sudo systemctl status ai-chat-app.service
```

## �📞 Support & FAQ

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
