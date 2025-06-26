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
    
    # Create chat sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create chat history table (updated with session_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            user_id INTEGER,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES chat_sessions (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Migration: Add session_id column if it doesn't exist
    try:
        cursor.execute("PRAGMA table_info(chat_messages)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'session_id' not in column_names:
            print("🔄 Migrating database: Adding session_id column...")
            cursor.execute('ALTER TABLE chat_messages ADD COLUMN session_id INTEGER')
            
            # For existing messages, create default sessions
            cursor.execute('SELECT DISTINCT user_id FROM chat_messages WHERE session_id IS NULL')
            users_with_messages = cursor.fetchall()
            
            for (user_id,) in users_with_messages:
                cursor.execute('''
                    INSERT INTO chat_sessions (user_id, title, created_at, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ''', (user_id, 'Migrated Chat'))
                
                session_id = cursor.lastrowid
                cursor.execute('''
                    UPDATE chat_messages 
                    SET session_id = ? 
                    WHERE user_id = ? AND session_id IS NULL
                ''', (session_id, user_id))
            
            print("✅ Database migration completed!")
    except Exception as e:
        print(f"Migration check failed: {e}")
    
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
        return "🔌 Unable to connect to AI service. Please start Ollama with Docker using 'docker-compose up -d ollama'."
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

# Session management functions
def get_or_create_default_session(user_id):
    """Get or create a default chat session for user"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Try to get existing default session
    cursor.execute('''
        SELECT id FROM chat_sessions 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    ''', (user_id,))
    
    session_row = cursor.fetchone()
    
    if session_row:
        session_id = session_row[0]
    else:
        # Create new default session
        cursor.execute('''
            INSERT INTO chat_sessions (user_id, title)
            VALUES (?, ?)
        ''', (user_id, 'New Chat'))
        session_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return session_id

def verify_session_ownership(session_id, user_id):
    """Verify that a session belongs to the user"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM chat_sessions 
        WHERE id = ? AND user_id = ?
    ''', (session_id, user_id))
    
    result = cursor.fetchone()
    conn.close()
    return result is not None

def create_new_session(user_id, title="New Chat"):
    """Create a new chat session"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO chat_sessions (user_id, title)
        VALUES (?, ?)
    ''', (user_id, title))
    
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_user_sessions(user_id):
    """Get all chat sessions for a user with recent message preview"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.id, s.title, s.created_at, s.updated_at,
               (SELECT COUNT(*) FROM chat_messages WHERE session_id = s.id) as message_count,
               (SELECT message FROM chat_messages WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1) as last_user_message,
               (SELECT response FROM chat_messages WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1) as last_ai_response
        FROM chat_sessions s
        WHERE s.user_id = ?
        ORDER BY s.updated_at DESC
    ''', (user_id,))
    
    sessions = cursor.fetchall()
    conn.close()
    
    result = []
    for session in sessions:
        last_message = session[5] if session[5] else None
        last_response = session[6] if session[6] else None
        
        # Create a conversation preview
        if last_message and last_response:
            # Show both user message and AI response
            preview = f"You: {last_message[:40]}{'...' if len(last_message) > 40 else ''}\nAI: {last_response[:40]}{'...' if len(last_response) > 40 else ''}"
        elif last_message:
            # Only user message exists
            preview = f"You: {last_message[:60]}{'...' if len(last_message) > 60 else ''}"
        else:
            preview = 'No messages yet'
            
        result.append({
            'id': session[0],
            'title': session[1],
            'created_at': session[2],
            'updated_at': session[3],
            'message_count': session[4],
            'last_message': preview
        })
    
    return result

def update_session_title(session_id, title):
    """Update session title"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE chat_sessions 
        SET title = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (title, session_id))
    
    conn.commit()
    conn.close()

def update_session_timestamp(session_id):
    """Update session's last activity timestamp"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE chat_sessions 
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (session_id,))
    
    conn.commit()
    conn.close()

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
@app.route('/chat/<int:session_id>')
def chat(session_id=None):
    """Main chat interface"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # If no session_id provided, get or create default session
    if not session_id:
        session_id = get_or_create_default_session(session['user_id'])
        return redirect(url_for('chat', session_id=session_id))
    
    # Verify session belongs to user
    if not verify_session_ownership(session_id, session['user_id']):
        return redirect(url_for('chat'))
    
    return render_template('chat.html', 
                         username=session.get('username'),
                         email=session.get('email'),
                         phone=session.get('phone', ''),
                         current_session_id=session_id)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat messages"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    message = data.get('message')
    session_id = data.get('session_id')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    if not session_id:
        return jsonify({'error': 'No session ID provided'}), 400
    
    # Verify session ownership
    if not verify_session_ownership(session_id, session['user_id']):
        return jsonify({'error': 'Invalid session'}), 403
    
    # Get AI response
    ai_response = get_ai_response(message)
    
    # Save to database
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_messages (session_id, user_id, message, response)
            VALUES (?, ?, ?, ?)
        ''', (session_id, session['user_id'], message, ai_response))
        
        # Update session timestamp
        update_session_timestamp(session_id)
        
        # Auto-generate title for new sessions
        cursor.execute('SELECT COUNT(*) FROM chat_messages WHERE session_id = ?', (session_id,))
        message_count = cursor.fetchone()[0]
        
        if message_count == 1:  # First message in session
            # Generate title from first message (first 50 chars)
            title = message[:50] + "..." if len(message) > 50 else message
            update_session_title(session_id, title)
        
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

@app.route('/api/chat-history/<int:session_id>')
def chat_history(session_id):
    """Get chat history for a specific session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify session ownership
    if not verify_session_ownership(session_id, session['user_id']):
        return jsonify({'error': 'Invalid session'}), 403
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT message, response, created_at 
        FROM chat_messages 
        WHERE session_id = ? 
        ORDER BY created_at ASC
    ''', (session_id,))
    
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

@app.route('/api/clear-chat-history/<int:session_id>', methods=['POST'])
def clear_chat_history(session_id):
    """Clear chat history for a specific session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify session ownership
    if not verify_session_ownership(session_id, session['user_id']):
        return jsonify({'error': 'Invalid session'}), 403
    
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM chat_messages 
            WHERE session_id = ?
        ''', (session_id,))
        
        # Reset session title
        update_session_title(session_id, 'New Chat')
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Chat history cleared'})
    except Exception as e:
        print(f"Error clearing chat history: {e}")
        return jsonify({'error': 'Failed to clear chat history'}), 500

@app.route('/api/sessions')
def get_sessions():
    """Get all chat sessions for the user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    sessions = get_user_sessions(session['user_id'])
    return jsonify({'sessions': sessions})

@app.route('/api/sessions/new', methods=['POST'])
def create_session():
    """Create a new chat session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json() if request.is_json else {}
    title = data.get('title', 'New Chat')
    
    session_id = create_new_session(session['user_id'], title)
    return jsonify({'session_id': session_id, 'title': title})

@app.route('/api/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a chat session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify session ownership
    if not verify_session_ownership(session_id, session['user_id']):
        return jsonify({'error': 'Invalid session'}), 403
    
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        # Delete messages first (foreign key constraint)
        cursor.execute('DELETE FROM chat_messages WHERE session_id = ?', (session_id,))
        
        # Delete session
        cursor.execute('DELETE FROM chat_sessions WHERE id = ?', (session_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting session: {e}")
        return jsonify({'error': 'Failed to delete session'}), 500

@app.route('/api/sessions/<int:session_id>/rename', methods=['POST'])
def rename_session(session_id):
    """Rename a chat session"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Verify session ownership
    if not verify_session_ownership(session_id, session['user_id']):
        return jsonify({'error': 'Invalid session'}), 403
    
    data = request.get_json()
    new_title = data.get('title', '').strip()
    
    if not new_title:
        return jsonify({'error': 'Title cannot be empty'}), 400
    
    update_session_title(session_id, new_title)
    return jsonify({'success': True, 'title': new_title})

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
