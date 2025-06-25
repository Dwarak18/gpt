#!/usr/bin/env python3
"""
Demo script to test the AI Chat App functionality
"""

import requests
import json
import time

def test_app():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing AI Chat App...")
    print("=" * 40)
    
    # Test 1: Check if app is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code in [200, 302]:  # 302 for redirect to login
            print("✅ Flask app is running")
        else:
            print(f"❌ App returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on localhost:5000")
        return False
    
    # Test 2: Check Ollama health endpoint
    try:
        response = requests.get(f"{base_url}/api/health/ollama", timeout=10)
        data = response.json()
        
        if response.status_code == 200 and data.get('status') == 'healthy':
            print("✅ Ollama AI service is healthy")
            print(f"   📊 Models available: {data.get('models_available', 0)}")
            print(f"   🤖 Required model: {'✅' if data.get('required_model_available') else '❌'}")
        else:
            print("⚠️  Ollama AI service is not healthy")
            print(f"   Error: {data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error checking Ollama health: {e}")
    
    # Test 3: Try to access login page
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("✅ Login page is accessible")
        else:
            print(f"❌ Login page returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing login page: {e}")
    
    # Test 4: Try to access signup page
    try:
        response = requests.get(f"{base_url}/signup", timeout=5)
        if response.status_code == 200:
            print("✅ Signup page is accessible")
        else:
            print(f"❌ Signup page returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing signup page: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Test Summary:")
    print("   If all tests pass, your app is ready!")
    print("   Open http://localhost:5000 in your browser")
    print("   Create an account and start chatting with AI!")
    
    return True

if __name__ == "__main__":
    print("🚀 AI Chat App - Demo Test")
    print("Make sure the Flask app is running first!")
    print("Run: python app.py")
    print()
    
    input("Press Enter when the app is running...")
    test_app()
