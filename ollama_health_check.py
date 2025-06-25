#!/usr/bin/env python3
"""
Ollama Health Checker and Model Installer
This script helps diagnose and fix Ollama connection issues.
"""

import requests
import time
import json
import subprocess
import sys
import os

OLLAMA_URL = "http://localhost:11434"
REQUIRED_MODEL = "llama3.2:1b-instruct-q4_K_M"

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_ollama_container():
    """Check if Ollama container is running"""
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=ollama-server', '--format', '{{.Status}}'], 
                              capture_output=True, text=True)
        return 'Up' in result.stdout
    except:
        return False

def start_ollama_container():
    """Start Ollama container using docker-compose"""
    try:
        print("🚀 Starting Ollama container...")
        result = subprocess.run(['docker-compose', 'up', '-d', 'ollama'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_ollama_health():
    """Check if Ollama service is responding"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_available_models():
    """Get list of available models"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model.get('name', '') for model in data.get('models', [])]
        return []
    except:
        return []

def pull_model(model_name):
    """Pull a model using docker exec"""
    try:
        print(f"📥 Pulling model {model_name}...")
        print("This may take several minutes depending on your internet connection...")
        result = subprocess.run(['docker', 'exec', 'ollama-server', 'ollama', 'pull', model_name], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def test_model(model_name):
    """Test if model responds correctly"""
    try:
        payload = {
            "model": model_name,
            "prompt": "Hello! Please respond with 'AI connection successful!'",
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('response', '').strip()
        return None
    except:
        return None

def main():
    print("🔧 Ollama Health Checker & Setup Tool")
    print("=" * 40)
    
    # Step 1: Check Docker
    print("1️⃣ Checking Docker...")
    if not check_docker():
        print("❌ Docker is not running or not installed.")
        print("Please install Docker and make sure it's running.")
        return False
    print("✅ Docker is running")
    
    # Step 2: Check Ollama container
    print("\n2️⃣ Checking Ollama container...")
    if not check_ollama_container():
        print("⚠️ Ollama container is not running. Starting it...")
        if not start_ollama_container():
            print("❌ Failed to start Ollama container.")
            print("Try running: docker-compose up -d ollama")
            return False
        
        # Wait for container to be ready
        print("⏳ Waiting for container to start...")
        time.sleep(10)
    
    print("✅ Ollama container is running")
    
    # Step 3: Check Ollama service
    print("\n3️⃣ Checking Ollama service...")
    max_attempts = 20
    for attempt in range(max_attempts):
        if check_ollama_health():
            print("✅ Ollama service is responding")
            break
        print(f"⏳ Waiting for Ollama service... ({attempt + 1}/{max_attempts})")
        time.sleep(3)
    else:
        print("❌ Ollama service is not responding after waiting.")
        print("Check container logs: docker-compose logs ollama")
        return False
    
    # Step 4: Check available models
    print("\n4️⃣ Checking available models...")
    available_models = get_available_models()
    print(f"📋 Available models: {available_models}")
    
    if REQUIRED_MODEL not in available_models:
        print(f"⚠️ Required model '{REQUIRED_MODEL}' not found.")
        print("Attempting to pull the model...")
        
        if not pull_model(REQUIRED_MODEL):
            print(f"❌ Failed to pull model '{REQUIRED_MODEL}'")
            return False
        
        print(f"✅ Model '{REQUIRED_MODEL}' pulled successfully")
    else:
        print(f"✅ Required model '{REQUIRED_MODEL}' is available")
    
    # Step 5: Test the model
    print("\n5️⃣ Testing AI model...")
    response = test_model(REQUIRED_MODEL)
    
    if response:
        print("✅ AI model test successful!")
        print(f"🤖 AI Response: {response}")
        print("\n🎉 Setup complete! Your Flask app should now be able to connect to Ollama.")
        print(f"\n📋 Configuration Summary:")
        print(f"   - Ollama URL: {OLLAMA_URL}")
        print(f"   - Model: {REQUIRED_MODEL}")
        print(f"   - Container: ollama-server")
        return True
    else:
        print("❌ AI model test failed")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ All checks passed! You can now run your Flask app.")
