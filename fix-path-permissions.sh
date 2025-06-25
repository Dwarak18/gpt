#!/bin/bash
# fix-path-permissions.sh - Fix directory path permissions for Apache

echo "🔧 Fixing directory path permissions for Apache..."
echo "================================================="

# Fix permissions on parent directories
echo "📂 Setting execute permissions on parent directories..."

# Give execute permission to /home directory
sudo chmod 755 /home

# Give execute permission to /home/gpt-lama directory
sudo chmod 755 /home/gpt-lama

# Give full access to the project directory
sudo chmod 755 /home/gpt-lama/gpt

# Set ownership and permissions recursively for the project
echo "👥 Setting ownership and permissions for project files..."
sudo chown -R www-data:www-data /home/gpt-lama/gpt
sudo find /home/gpt-lama/gpt -type d -exec chmod 755 {} \;
sudo find /home/gpt-lama/gpt -type f -exec chmod 644 {} \;

# Make WSGI file executable
sudo chmod 755 /home/gpt-lama/gpt/app.wsgi

# Create and set permissions for static directory
if [ ! -d "/home/gpt-lama/gpt/static" ]; then
    echo "📁 Creating static directory..."
    mkdir -p /home/gpt-lama/gpt/static
fi
sudo chown -R www-data:www-data /home/gpt-lama/gpt/static
sudo chmod -R 755 /home/gpt-lama/gpt/static

# Test current permissions
echo "🔍 Checking current permissions..."
ls -la /home/
ls -la /home/gpt-lama/
ls -la /home/gpt-lama/gpt/

# Test Apache configuration
echo "🧪 Testing Apache configuration..."
sudo apache2ctl configtest

if [ $? -eq 0 ]; then
    echo "✅ Apache configuration is valid!"
    
    # Restart Apache
    echo "🔄 Restarting Apache..."
    sudo systemctl restart apache2
    
    echo "🎉 Path permissions fixed successfully!"
    echo "======================================"
    echo "📋 Your Flask app should now be accessible at:"
    echo "   - http://20.192.16.3"
    echo "   - http://10.0.0.4"
    echo ""
    echo "🔍 Monitor for any remaining issues:"
    echo "   sudo tail -f /var/log/apache2/flaskapp_error.log"
else
    echo "❌ Apache configuration has errors."
    echo "🔍 Check error log: sudo tail -f /var/log/apache2/error.log"
fi

echo ""
echo "📋 Directory permissions summary:"
echo "   /home (755 - readable/executable by all)"
echo "   /home/gpt-lama (755 - readable/executable by all)"
echo "   /home/gpt-lama/gpt (755 - owned by www-data)"
