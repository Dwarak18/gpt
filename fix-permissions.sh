#!/bin/bash
# fix-permissions.sh - Fix Apache permissions for Flask app

echo "🔧 Fixing Apache permissions for Flask app..."
echo "============================================="

# Get the current working directory
CURRENT_DIR=$(pwd)
echo "📁 Current directory: $CURRENT_DIR"

# Set correct ownership
echo "👥 Setting ownership to www-data..."
sudo chown -R www-data:www-data "$CURRENT_DIR"

# Set directory permissions (755 = rwxr-xr-x)
echo "📂 Setting directory permissions..."
sudo find "$CURRENT_DIR" -type d -exec chmod 755 {} \;

# Set file permissions (644 = rw-r--r--)
echo "📄 Setting file permissions..."
sudo find "$CURRENT_DIR" -type f -exec chmod 644 {} \;

# Make WSGI file executable
echo "🔧 Making WSGI file executable..."
sudo chmod 755 "$CURRENT_DIR/app.wsgi"

# Create static directory if it doesn't exist
if [ ! -d "$CURRENT_DIR/static" ]; then
    echo "📁 Creating static directory..."
    mkdir -p "$CURRENT_DIR/static"
    sudo chown www-data:www-data "$CURRENT_DIR/static"
    sudo chmod 755 "$CURRENT_DIR/static"
fi

# Update Apache configuration with correct path
echo "⚙️ Updating Apache configuration..."
sudo sed -i "s|/home/gpt-lama/gpt|$CURRENT_DIR|g" /etc/apache2/sites-available/apache-flaskapp.conf

# Update WSGI file with correct path
echo "📝 Updating WSGI file..."
sudo sed -i "s|/home/gpt-lama/gpt|$CURRENT_DIR|g" "$CURRENT_DIR/app.wsgi"

# Test Apache configuration
echo "🧪 Testing Apache configuration..."
sudo apache2ctl configtest

if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid!"
    
    # Reload Apache configuration
    echo "🔄 Reloading Apache..."
    sudo systemctl reload apache2
    
    echo "🎉 Permissions fixed successfully!"
    echo "================================="
    echo "📋 Your Flask app should now be accessible at:"
    echo "   - http://20.192.16.3"
    echo "   - http://10.0.0.4"
    echo ""
    echo "🔍 To debug any remaining issues:"
    echo "   sudo tail -f /var/log/apache2/flaskapp_error.log"
else
    echo "❌ Apache configuration has errors. Please check the logs."
    echo "🔍 Check error log: sudo tail -f /var/log/apache2/error.log"
fi
