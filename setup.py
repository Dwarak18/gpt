"""
Setup script for AI Chat App
Automates the installation and setup process
"""

import subprocess
import sys
import os
import requests
import json

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python():
    """Check if Python is installed and version is compatible"""
    print("🐍 Checking Python installation...")
    try:
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} is too old. Need Python 3.8+")
            return False
    except Exception as e:
        print(f"❌ Error checking Python version: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def check_ollama():
    """Check if Ollama is installed and running"""
    print("🤖 Checking Ollama installation...")
    
    # Check if Ollama command exists
    try:
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
        else:
            print("❌ Ollama is not installed")
            print("   Please install from: https://ollama.com")
            return False
    except Exception:
        print("❌ Ollama is not installed or not in PATH")
        print("   Please install from: https://ollama.com")
        return False
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service is running")
            
            # Check if required model is available
            data = response.json()
            models = data.get('models', [])
            required_model = "llama3.2:1b-instruct-q4_K_M"
            
            has_model = any(model.get('name') == required_model for model in models)
            
            if has_model:
                print("✅ Required AI model is available")
                return True
            else:
                print("⚠️  Required AI model is not downloaded")
                print(f"   Run: ollama pull {required_model}")
                
                # Offer to download the model
                download = input("   Download the model now? (y/n): ").lower().strip()
                if download == 'y':
                    return run_command(f"ollama pull {required_model}", "Downloading AI model")
                return False
        else:
            print("❌ Ollama service is not responding")
            print("   Start Ollama with: ollama serve")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama service")
        print("   Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False

def setup_database():
    """Initialize the database"""
    print("🗄️  Setting up database...")
    try:
        # Import and run the init_db function
        from app import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AI Chat App - Setup Script")
    print("=" * 50)
    
    # Step 1: Check Python
    if not check_python():
        print("\n❌ Setup failed: Python version incompatible")
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return False
    
    # Step 3: Check Ollama
    if not check_ollama():
        print("\n⚠️  Setup completed with warnings: Ollama not fully configured")
        print("   The app will work, but AI features will be limited")
    
    # Step 4: Setup database
    if not setup_database():
        print("\n❌ Setup failed: Could not initialize database")
        return False
    
    # Success message
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n🚀 To start the application:")
    print("   python app.py")
    print("\n🌐 Then open your browser to:")
    print("   http://localhost:5000")
    print("\n📋 Quick start:")
    print("   1. Run: python app.py")
    print("   2. Open http://localhost:5000")
    print("   3. Sign up for a new account")
    print("   4. Start chatting with AI!")
    
    return True

if __name__ == "__main__":
    main()
