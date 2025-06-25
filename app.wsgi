#!/usr/bin/python3
"""
WSGI configuration for AI Chat App
This file is used by Apache mod_wsgi to serve the Flask application
"""

import sys
import os

# Add your project directory to the Python path
sys.path.insert(0, "/home/gpt-lama/gpt/")

# Change to your project directory
os.chdir("/home/gpt-lama/gpt/")

# Import your Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
