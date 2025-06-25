#!/bin/bash
# setup-apache.sh - Setup script for Apache with Flask app

echo "🚀 Setting up Flask App with Apache..."
echo "===================================="

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Install Apache and mod_wsgi
echo "🔧 Installing Apache and mod_wsgi..."
sudo apt install -y apache2 libapache2-mod-wsgi-py3

# Enable mod_wsgi
echo "✅ Enabling mod_wsgi..."
sudo a2enmod wsgi
sudo a2enmod headers

# Copy Apache configuration
echo "📄 Setting up Apache virtual host..."
sudo cp apache-flaskapp.conf /etc/apache2/sites-available/

# Enable the site
sudo a2ensite apache-flaskapp.conf

# Disable default Apache site (optional)
sudo a2dissite 000-default.conf

# Set correct permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /home/gpt-lama/gpt
sudo chmod -R 755 /home/gpt-lama/gpt

# Create a systemd service for better management (optional)
echo "🛠️ Creating systemd service..."
sudo tee /etc/systemd/system/ollama-flask.service > /dev/null <<EOF
[Unit]
Description=Ollama Flask AI Chat App
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/home/gpt-lama/gpt
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 /home/gpt-lama/gpt/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Test Apache configuration
echo "🧪 Testing Apache configuration..."
sudo apache2ctl configtest

if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid!"
    
    # Restart Apache
    echo "🔄 Restarting Apache..."
    sudo systemctl restart apache2
    sudo systemctl enable apache2
    
    echo "🎉 Setup complete!"
    echo "=================================="
    echo "📋 Your Flask app should now be accessible at:"
    echo "   - http://20.192.16.3"
    echo "   - http://10.0.0.4"
    echo ""
    echo "🔍 To check status:"
    echo "   sudo systemctl status apache2"
    echo "   sudo tail -f /var/log/apache2/flaskapp_error.log"
    echo ""
    echo "🐳 Don't forget to start Ollama:"
    echo "   docker-compose up -d ollama"
    echo "   docker exec ollama-server ollama pull llama3.2:1b-instruct-q4_K_M"
else
    echo "❌ Apache configuration has errors. Please check the configuration file."
fi
