# 🤖 AI Chat App with Flask

A beautiful and modern AI chat application built with Flask, featuring user authentication, real-time chat with AI, and a responsive design inspired by the GPT-llama3.2 repository.

## ✨ Features

- 🔐 **User Authentication**: Secure login and signup with password hashing
- 💬 **AI Chat Interface**: Real-time chat with Ollama AI model
- 👤 **User Profiles**: Personal profile management
- 📱 **Responsive Design**: Beautiful UI that works on all devices
- 🎨 **Modern UI**: Gradient backgrounds, glassmorphism effects, and smooth animations
- 📊 **Chat History**: Track your conversations with the AI
- 🔄 **Connection Status**: Real-time AI service status monitoring

## 🛠️ Prerequisites

Before running the application, make sure you have:

1. **Python 3.8+** installed
2. **Ollama** installed and running with the `llama3.2:1b-instruct-q4_K_M` model
3. **Git** (optional, for cloning)

### Installing Ollama

1. Download Ollama from [https://ollama.com/](https://ollama.com/)
2. Install Ollama on your system
3. Pull the required model:
   ```bash
   ollama pull llama3.2:1b-instruct-q4_K_M
   ```
4. Keep Ollama running in the background:
   ```bash
   ollama serve
   ```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker Desktop (for Ollama)
- Git (optional)

### 🐳 Docker-based Setup (Recommended)

1. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Make sure Docker is running

2. **Clone or Download the project**
   ```bash
   git clone <repository-url>
   cd GPT-llama
   ```

3. **One-click setup and run**
   ```bash
   # Windows - Complete setup with Ollama
   start-with-ollama.bat
   
   # This script will:
   # - Check Docker
   # - Start Ollama container
   # - Download llama3.2:1b-instruct-q4_K_M model
   # - Install Python dependencies  
   # - Start the Flask app
   ```

4. **Manual Docker setup (if needed)**
   ```bash
   # Setup Ollama with Docker only
   setup-ollama.bat
   
   # Then start the Flask app
   start.bat
   ```

### 🔧 Traditional Setup (Alternative)

1. **Install Ollama locally**
   - Download from https://ollama.ai
   - Install and start Ollama service
   - Pull the model: `ollama pull llama3.2:1b-instruct-q4_K_M`

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

### 4. Access the Application
Open your browser and navigate to: `http://localhost:5000`

## 📋 How to Use

### First Time Setup
1. **Start Ollama**: Make sure Ollama is running with the required model
2. **Run the Flask app**: `python app.py`
3. **Open your browser**: Go to `http://localhost:5000`
4. **Sign Up**: Create a new account
5. **Login**: Use your credentials to login
6. **Start Chatting**: Begin your conversation with the AI!

### Using the Chat Interface
- **Send Messages**: Type your message and press Enter or click the send button
- **AI Responses**: The AI will respond to your messages in real-time
- **Connection Status**: Check the status indicator to see if AI is connected
- **Profile**: Click on your username to view/edit your profile
- **Logout**: Use the dropdown menu to logout

## 🔧 Configuration

### Environment Variables
You can customize the application by setting these environment variables:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///chatapp.db

# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b-instruct-q4_K_M
```

### Customization
- **AI Model**: Change the model in `app.py` by modifying the `OLLAMA_MODEL` variable
- **Styling**: Modify the CSS in the template files to customize the appearance
- **Database**: The app uses SQLite by default, but you can modify it to use other databases

## 📁 Project Structure

```
GPT-llama/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── chatapp.db            # SQLite database (created automatically)
└── templates/            # HTML templates
    ├── base.html         # Base template with common styles
    ├── login.html        # Login page
    ├── signup.html       # Signup page
    ├── chat.html         # Main chat interface
    └── profile.html      # User profile page
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Unable to connect to AI service"
- **Solution**: Make sure Ollama is running and accessible at `http://localhost:11434`
- **Check**: Run `ollama list` to verify the model is installed

#### 2. "AI service is currently unavailable"
- **Solution**: Restart Ollama service
- **Check**: Verify the model name matches exactly: `llama3.2:1b-instruct-q4_K_M`

#### 3. "Import Error" when running the app
- **Solution**: Install missing dependencies: `pip install -r requirements.txt`

#### 4. Database errors
- **Solution**: Delete `chatapp.db` and restart the app to recreate the database

#### 5. Port already in use
- **Solution**: Change the port in `app.py` by modifying `app.run(port=5000)` to a different port

### Testing Ollama Connection
You can test if Ollama is working correctly:

```bash
# Test if Ollama is running
curl http://localhost:11434/api/tags

# Test the specific model
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b-instruct-q4_K_M",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

## 🎨 Customization

### Changing the AI Model
1. Pull a different model: `ollama pull <model-name>`
2. Update the model name in `app.py`:
   ```python
   "model": "your-model-name-here"
   ```

### Styling Customization
- Modify CSS variables in `templates/base.html` to change colors and themes
- Update individual template files for specific page styling
- Add custom JavaScript for additional functionality

### Adding Features
- **Chat History**: Extend the database schema to store more chat metadata
- **File Uploads**: Add support for image/file uploads to the AI
- **User Roles**: Implement admin/user roles
- **Chat Rooms**: Add support for multiple chat rooms

## 🚀 Deployment

### Local Deployment
The app is ready to run locally as described in the Quick Start section.

### Production Deployment
For production deployment:

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=False
   ```

2. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up a reverse proxy** (nginx, Apache)
4. **Use a production database** (PostgreSQL, MySQL)

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Make sure Ollama is properly installed and running
3. Verify all dependencies are installed correctly

## 🎯 Inspired By

This project is inspired by the [GPT-llama3.2](https://github.com/Dwarak18/GPT-llama3.2) repository, recreated as a simplified Flask application with modern UI design.

---

**Enjoy chatting with your AI assistant! 🤖✨**
