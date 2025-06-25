from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import requests
from datetime import timedelta
import json

# Import configuration
try:
    from config import *
except ImportError:
    # Default configuration if config.py is not found
    FLASK_HOST = "0.0.0.0"
    FLASK_PORT = 8888
    FLASK_DEBUG = True
    SECRET_KEY = "your-secret-key-here-change-in-production"
    DATABASE_NAME = "chatapp.db"
    OLLAMA_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.2:1b-instruct-q4_K_M"
    OLLAMA_TIMEOUT = 30
    SESSION_LIFETIME_HOURS = 1
    APP_NAME = "AI Chat App"
    APP_TITLE = "🤖 AI Chat Assistant"
    WELCOME_MESSAGE = "Hello! I'm your AI assistant. How can I help you today? 🚀"

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=SESSION_LIFETIME_HOURS)

# Database initialization
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Ollama integration functions
def get_ai_response(message):
    """Get response from Ollama AI model"""
    try:
        ollama_url = f"{OLLAMA_URL}/api/generate"
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": message,
            "stream": False
        }
        
        print(f"🤖 Sending request to Ollama: {ollama_url}")
        print(f"📝 Model: {OLLAMA_MODEL}")
        
        response = requests.post(ollama_url, json=payload, timeout=OLLAMA_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('response', 'No response from AI model.')
            print(f"✅ AI Response received: {len(ai_response)} characters")
            return ai_response
        elif response.status_code == 404:
            return f"❌ Model '{OLLAMA_MODEL}' not found. Please run the setup script to install the model."
        else:
            print(f"❌ Ollama API error: {response.status_code} - {response.text}")
            return f"AI service error (HTTP {response.status_code}). Please check if the model is available."
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return "🔌 Unable to connect to AI service. Please run 'setup-ollama.bat' to start Ollama with Docker."
    except requests.exceptions.Timeout as e:
        print(f"⏱️ Timeout error: {e}")
        return "⏱️ AI service is taking too long to respond. The model might be loading. Please try again in a moment."
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return f"❌ Error communicating with AI service: {str(e)}"

def check_ollama_health():
    """Check if Ollama service is healthy"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            has_required_model = any(model.get('name') == OLLAMA_MODEL for model in models)
            return {
                'status': 'healthy',
                'models_available': len(models),
                'required_model_available': has_required_model,
                'models': [model.get('name') for model in models]
            }
        return {'status': 'unhealthy', 'error': 'Service unavailable'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}

# Routes
@app.route('/')
def index():
    """Main route - redirect to login if not authenticated"""
    if 'user_id' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username_or_email = data.get('usernameOrEmail')
        password = data.get('password')
        
        if not username_or_email or not password:
            if request.is_json:
                return jsonify({'error': 'Missing fields'}), 400
            return render_template('login.html', error='Missing fields')
        
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Check if user exists by username or email
        cursor.execute('''
            SELECT id, username, email, password_hash, phone 
            FROM users 
            WHERE username = ? OR email = ?
        ''', (username_or_email, username_or_email))
        
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session.permanent = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            session['phone'] = user[4]
            
            if request.is_json:
                return jsonify({
                    'message': 'Login successful',
                    'userId': user[0],
                    'username': user[1],
                    'email': user[2],
                    'phone': user[4] or ''
                })
            return redirect(url_for('chat'))
        else:
            if request.is_json:
                return jsonify({'error': 'Invalid credentials'}), 401
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and user registration"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', '')
        
        if not username or not email or not password:
            if request.is_json:
                return jsonify({'error': 'Missing fields'}), 400
            return render_template('signup.html', error='Missing fields')
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, phone)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, phone))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            if request.is_json:
                return jsonify({'message': 'User created', 'userId': user_id}), 201
            return redirect(url_for('login'))
            
        except sqlite3.IntegrityError:
            if request.is_json:
                return jsonify({'error': 'User already exists or invalid data'}), 400
            return render_template('signup.html', error='Username or email already exists')
    
    return render_template('signup.html')

@app.route('/chat')
def chat():
    """Main chat interface"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('chat.html', 
                         username=session.get('username'),
                         email=session.get('email'),
                         phone=session.get('phone', ''))

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat messages"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get AI response
    ai_response = get_ai_response(message)
    
    # Save to database
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (user_id, message, response)
            VALUES (?, ?, ?)
        ''', (session['user_id'], message, ai_response))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving chat message: {e}")
    
    return jsonify({'reply': ai_response})

@app.route('/api/health/ollama')
def health_ollama():
    """Health check for Ollama service"""
    health_status = check_ollama_health()
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

@app.route('/api/chat-history')
def chat_history():
    """Get user's chat history"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT message, response, created_at 
        FROM chat_messages 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 50
    ''', (session['user_id'],))
    
    messages = cursor.fetchall()
    conn.close()
    
    chat_history = []
    for msg in messages:
        chat_history.append({
            'user_message': msg[0],
            'ai_response': msg[1],
            'timestamp': msg[2]
        })
    
    return jsonify({'history': chat_history})

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('profile.html',
                         username=session.get('username'),
                         email=session.get('email'),
                         phone=session.get('phone', ''))

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    print("🚀 Starting AI Chat App...")
    print(f"📡 Server: http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"🤖 Ollama URL: {OLLAMA_URL}")
    print(f"🧠 AI Model: {OLLAMA_MODEL}")
    print("=" * 50)
    
    # Run the application
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
