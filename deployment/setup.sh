#!/bin/bash

###############################################################################
# AgroGhala VPS Deployment Script
# This script sets up the application on a Linux VPS with systemd and nginx
###############################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="agrosoko"
APP_DIR="/var/www/agrosoko.ai"
APP_USER="www-data"
PYTHON_VERSION="3.11"
DOMAIN="your-domain.com"  # Change this to your domain

echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   AgroGhala VPS Deployment Setup${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Step 1: Update system packages${NC}"
apt update
apt upgrade -y

echo -e "\n${YELLOW}Step 2: Install required packages${NC}"
apt install -y python3.11 python3.11-venv python3-pip nginx git curl supervisor certbot python3-certbot-nginx

echo -e "\n${YELLOW}Step 3: Create application directory${NC}"
mkdir -p $APP_DIR
mkdir -p /var/log/agrosoko
chown -R $APP_USER:$APP_USER $APP_DIR
chown -R $APP_USER:$APP_USER /var/log/agrosoko

echo -e "\n${YELLOW}Step 4: Copy application files${NC}"
echo "Please ensure your application code is in $APP_DIR"
echo "You can use: rsync -avz --exclude 'venv' --exclude '__pycache__' ./ user@server:$APP_DIR/"
read -p "Press enter when files are copied..."

echo -e "\n${YELLOW}Step 5: Set up Python virtual environment${NC}"
cd $APP_DIR
sudo -u $APP_USER python3.11 -m venv venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements.txt

echo -e "\n${YELLOW}Step 6: Configure environment variables${NC}"
if [ ! -f "$APP_DIR/.env" ]; then
    echo "Creating .env file..."
    cat > $APP_DIR/.env << EOF
# WhatsApp Configuration
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=your_verify_token

# Google Sheets Configuration
GOOGLE_SHEETS_CREDS_PATH=/var/www/agrosoko.ai/credentials/google-creds.json

# Weather API (optional)
OPENWEATHER_API_KEY=your_api_key_if_needed

# Application Settings
ENVIRONMENT=production
EOF
    chown $APP_USER:$APP_USER $APP_DIR/.env
    chmod 600 $APP_DIR/.env
    echo -e "${YELLOW}Please edit $APP_DIR/.env with your actual credentials${NC}"
    read -p "Press enter when done..."
fi

echo -e "\n${YELLOW}Step 7: Set up Google credentials (if needed)${NC}"
mkdir -p $APP_DIR/credentials
echo "Place your Google service account JSON in: $APP_DIR/credentials/google-creds.json"
read -p "Press enter when done (or skip if not using Google Sheets)..."

echo -e "\n${YELLOW}Step 8: Install systemd service${NC}"
cp deployment/agrosoko.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable agrosoko.service

echo -e "\n${YELLOW}Step 9: Configure nginx${NC}"
cp deployment/nginx.conf /etc/nginx/sites-available/agrosoko
ln -sf /etc/nginx/sites-available/agrosoko /etc/nginx/sites-enabled/

# Update domain in nginx config
sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/agrosoko

# Test nginx configuration
nginx -t

echo -e "\n${YELLOW}Step 10: Set up firewall${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo -e "\n${YELLOW}Step 11: Start services${NC}"
systemctl start agrosoko
systemctl restart nginx

echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"

echo -e "\n${YELLOW}Service Status:${NC}"
systemctl status agrosoko --no-pager

echo -e "\n${YELLOW}Useful Commands:${NC}"
echo "  Start service:    sudo systemctl start agrosoko"
echo "  Stop service:     sudo systemctl stop agrosoko"
echo "  Restart service:  sudo systemctl restart agrosoko"
echo "  View logs:        sudo journalctl -u agrosoko -f"
echo "  App logs:         tail -f /var/log/agrosoko/error.log"
echo "  Nginx logs:       tail -f /var/log/nginx/agrosoko_error.log"

echo -e "\n${YELLOW}Next Steps:${NC}"
echo "1. Update /etc/nginx/sites-available/agrosoko with your actual domain"
echo "2. Set up SSL: sudo certbot --nginx -d $DOMAIN"
echo "3. Test the API: curl http://localhost:8000"
echo "4. Configure your WhatsApp webhook to point to: https://$DOMAIN/webhook"

echo -e "\n${GREEN}Setup complete! 🚀${NC}"

