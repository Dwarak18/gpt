#!/bin/bash
# move-to-var-www.sh - Move Flask app to /var/www/

echo "📦 Moving Flask app to /var/www/..."
echo "=================================="

# Create the destination directory
sudo mkdir -p /var/www/flaskapp

# Copy all files
echo "📁 Copying files..."
sudo cp -r /home/gpt-lama/gpt/* /var/www/flaskapp/

# Set correct ownership and permissions
echo "👥 Setting ownership and permissions..."
sudo chown -R www-data:www-data /var/www/flaskapp
sudo chmod -R 755 /var/www/flaskapp
sudo find /var/www/flaskapp -type f -exec chmod 644 {} \;
sudo chmod 755 /var/www/flaskapp/app.wsgi

# Update WSGI file
echo "📝 Updating WSGI file..."
sudo sed -i 's|/home/gpt-lama/gpt|/var/www/flaskapp|g' /var/www/flaskapp/app.wsgi

# Create updated Apache configuration
echo "⚙️ Creating updated Apache configuration..."
sudo tee /etc/apache2/sites-available/flaskapp.conf > /dev/null <<EOF
<VirtualHost *:80>
    ServerName 20.192.16.3
    ServerAlias www.20.192.16.3
    DocumentRoot /var/www/flaskapp
    
    WSGIDaemonProcess flaskapp python-path=/var/www/flaskapp user=www-data group=www-data threads=5
    WSGIProcessGroup flaskapp
    WSGIScriptAlias / /var/www/flaskapp/app.wsgi
    
    <Directory /var/www/flaskapp>
        WSGIApplicationGroup %{GLOBAL}
        Order allow,deny
        Allow from all
        Require all granted
    </Directory>
    
    Alias /static /var/www/flaskapp/static
    <Directory /var/www/flaskapp/static>
        Order allow,deny
        Allow from all
        Require all granted
    </Directory>
    
    ErrorLog \${APACHE_LOG_DIR}/flaskapp_error.log
    CustomLog \${APACHE_LOG_DIR}/flaskapp_access.log combined
</VirtualHost>
EOF

# Disable old site and enable new one
echo "🔄 Updating Apache sites..."
sudo a2dissite apache-flaskapp.conf 2>/dev/null || true
sudo a2ensite flaskapp.conf

# Test and restart Apache
echo "🧪 Testing Apache configuration..."
sudo apache2ctl configtest

if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid!"
    sudo systemctl restart apache2
    
    echo "🎉 Flask app moved successfully!"
    echo "==============================="
    echo "📍 New location: /var/www/flaskapp"
    echo "📋 Accessible at:"
    echo "   - http://20.192.16.3"
    echo "   - http://10.0.0.4"
else
    echo "❌ Apache configuration has errors."
fi
EOF
