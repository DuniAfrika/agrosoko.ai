# AgroGhala VPS Deployment Guide

Complete guide for deploying the AgroGhala API on a Linux VPS with systemd and nginx.

## Prerequisites

- A Linux VPS (Ubuntu 20.04+ or Debian 11+ recommended)
- Root or sudo access
- A domain name pointed to your VPS (optional but recommended)
- Basic knowledge of Linux command line

## Quick Deployment

### Option 1: Automated Setup (Recommended)

1. **Copy files to your VPS:**
```bash
# From your local machine
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' \
  /Users/ratego/Dev/agrosoko.ai/ user@your-vps:/tmp/agrosoko-deploy/
```

2. **Run the setup script on VPS:**
```bash
# SSH into your VPS
ssh user@your-vps

# Move to root and run setup
sudo mv /tmp/agrosoko-deploy /var/www/agrosoko.ai
cd /var/www/agrosoko.ai
sudo bash deployment/setup.sh
```

### Option 2: Manual Setup

Follow the steps below for a detailed manual installation.

---

## Manual Deployment Steps

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.11 python3.11-venv python3-pip \
  nginx git curl supervisor certbot python3-certbot-nginx \
  build-essential libssl-dev libffi-dev
```

### 2. Create Application Directory

```bash
# Create directories
sudo mkdir -p /var/www/agrosoko.ai
sudo mkdir -p /var/log/agrosoko

# Set ownership
sudo chown -R www-data:www-data /var/www/agrosoko.ai
sudo chown -R www-data:www-data /var/log/agrosoko
```

### 3. Deploy Application Code

```bash
# Option A: Using rsync (from your local machine)
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' \
  /Users/ratego/Dev/agrosoko.ai/ user@your-vps:/var/www/agrosoko.ai/

# Option B: Using git (on VPS)
sudo -u www-data git clone https://github.com/yourusername/agrosoko.ai.git /var/www/agrosoko.ai
```

### 4. Set Up Python Environment

```bash
cd /var/www/agrosoko.ai

# Create virtual environment
sudo -u www-data python3.11 -m venv venv

# Install dependencies
sudo -u www-data ./venv/bin/pip install --upgrade pip
sudo -u www-data ./venv/bin/pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
# Create .env file
sudo nano /var/www/agrosoko.ai/.env
```

Add your configuration:

```env
# WhatsApp Configuration
WHATSAPP_TOKEN=your_actual_token_here
WHATSAPP_PHONE_ID=your_phone_id_here
WHATSAPP_VERIFY_TOKEN=your_verify_token_here

# Google Sheets Configuration
GOOGLE_SHEETS_CREDS_PATH=/var/www/agrosoko.ai/credentials/google-creds.json

# Weather API (Optional - has free fallback)
OPENWEATHER_API_KEY=your_api_key

# Application Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
```

Set proper permissions:
```bash
sudo chown www-data:www-data /var/www/agrosoko.ai/.env
sudo chmod 600 /var/www/agrosoko.ai/.env
```

### 6. Set Up Google Credentials (if using)

```bash
# Create credentials directory
sudo mkdir -p /var/www/agrosoko.ai/credentials

# Copy your Google service account JSON file
sudo nano /var/www/agrosoko.ai/credentials/google-creds.json
# Paste your credentials

# Set permissions
sudo chown www-data:www-data /var/www/agrosoko.ai/credentials/google-creds.json
sudo chmod 600 /var/www/agrosoko.ai/credentials/google-creds.json
```

### 7. Install Systemd Service

```bash
# Copy service file
sudo cp /var/www/agrosoko.ai/deployment/agrosoko.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable agrosoko.service

# Start the service
sudo systemctl start agrosoko.service

# Check status
sudo systemctl status agrosoko.service
```

### 8. Configure Nginx

```bash
# Copy nginx configuration
sudo cp /var/www/agrosoko.ai/deployment/nginx.conf /etc/nginx/sites-available/agrosoko

# Update domain name in config
sudo nano /etc/nginx/sites-available/agrosoko
# Change "your-domain.com" to your actual domain

# Enable site
sudo ln -sf /etc/nginx/sites-available/agrosoko /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 9. Configure Firewall

```bash
# Allow SSH (important!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 10. Set Up SSL (Let's Encrypt)

```bash
# Install certbot (if not already installed)
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

After SSL setup, uncomment the HTTPS server block in `/etc/nginx/sites-available/agrosoko` and restart nginx.

---

## Service Management

### Systemd Commands

```bash
# Start service
sudo systemctl start agrosoko

# Stop service
sudo systemctl stop agrosoko

# Restart service
sudo systemctl restart agrosoko

# Check status
sudo systemctl status agrosoko

# Enable on boot
sudo systemctl enable agrosoko

# Disable on boot
sudo systemctl disable agrosoko

# View logs (real-time)
sudo journalctl -u agrosoko -f

# View logs (last 100 lines)
sudo journalctl -u agrosoko -n 100
```

### Application Logs

```bash
# Access logs
tail -f /var/log/agrosoko/access.log

# Error logs
tail -f /var/log/agrosoko/error.log

# Nginx logs
tail -f /var/log/nginx/agrosoko_access.log
tail -f /var/log/nginx/agrosoko_error.log
```

### Nginx Commands

```bash
# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx

# Reload nginx (without dropping connections)
sudo systemctl reload nginx

# Check status
sudo systemctl status nginx
```

---

## Testing the Deployment

### 1. Local Test

```bash
# Test from VPS
curl http://localhost:8000

# Should return:
# {"status":"AgroGhala Agentic API is running","version":"1.0.0",...}
```

### 2. External Test

```bash
# From your local machine
curl http://your-domain.com

# Or with HTTPS (after SSL setup)
curl https://your-domain.com
```

### 3. Test API Endpoints

```bash
# Get counties
curl http://your-domain.com/api/counties

# Get weather
curl http://your-domain.com/api/weather/Nairobi

# Get prices
curl http://your-domain.com/api/prices

# View API docs
# Open in browser: https://your-domain.com/docs
```

---

## Updating the Application

### Method 1: Git Pull (if using git)

```bash
cd /var/www/agrosoko.ai
sudo -u www-data git pull origin main
sudo -u www-data ./venv/bin/pip install -r requirements.txt
sudo systemctl restart agrosoko
```

### Method 2: rsync (from local machine)

```bash
# From your local machine
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.env' \
  /Users/ratego/Dev/agrosoko.ai/ user@your-vps:/var/www/agrosoko.ai/

# Then on VPS
ssh user@your-vps
sudo systemctl restart agrosoko
```

---

## Monitoring

### System Resources

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check running processes
ps aux | grep uvicorn
```

### Application Health

```bash
# Check if service is running
sudo systemctl is-active agrosoko

# Check if service is enabled
sudo systemctl is-enabled agrosoko

# Check listening ports
sudo netstat -tlnp | grep 8000
# or
sudo ss -tlnp | grep 8000
```

### Log Rotation

Create log rotation configuration:

```bash
sudo nano /etc/logrotate.d/agrosoko
```

Add:

```
/var/log/agrosoko/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload agrosoko > /dev/null 2>&1 || true
    endscript
}
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check detailed logs
sudo journalctl -u agrosoko -n 50 --no-pager

# Check if port is already in use
sudo netstat -tlnp | grep 8000

# Check file permissions
ls -la /var/www/agrosoko.ai/

# Try running manually for debugging
cd /var/www/agrosoko.ai
sudo -u www-data ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Nginx Errors

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Check if nginx is running
sudo systemctl status nginx
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/agrosoko.ai
sudo chown -R www-data:www-data /var/log/agrosoko

# Fix .env permissions
sudo chmod 600 /var/www/agrosoko.ai/.env

# Fix data directory permissions
sudo chmod 755 /var/www/agrosoko.ai/data
```

### Application Errors

```bash
# Check application logs
tail -f /var/log/agrosoko/error.log

# Check Python dependencies
cd /var/www/agrosoko.ai
sudo -u www-data ./venv/bin/pip list

# Reinstall dependencies
sudo -u www-data ./venv/bin/pip install --force-reinstall -r requirements.txt
```

---

## Performance Tuning

### Uvicorn Workers

Edit `/etc/systemd/system/agrosoko.service`:

```ini
# For a VPS with 2 CPU cores, use 4-5 workers
ExecStart=/var/www/agrosoko.ai/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# For better performance, add:
# --worker-class uvicorn.workers.UvicornWorker
# --timeout-keep-alive 30
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl restart agrosoko
```

### Nginx Optimization

Add to nginx configuration:

```nginx
# Worker processes (match CPU cores)
worker_processes auto;

# Worker connections
events {
    worker_connections 1024;
}

# Gzip compression
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

---

## Backup Strategy

### Database Backup (if using database)

```bash
# Backup script
sudo nano /usr/local/bin/backup-agrosoko.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/agrosoko"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup data directory
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /var/www/agrosoko.ai/data/

# Backup .env
cp /var/www/agrosoko.ai/.env $BACKUP_DIR/env_$DATE

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

Make executable:
```bash
sudo chmod +x /usr/local/bin/backup-agrosoko.sh
```

Add to crontab:
```bash
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-agrosoko.sh
```

---

## Security Best Practices

1. **Keep system updated:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Use SSH key authentication** (disable password auth)

3. **Configure fail2ban:**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

4. **Regular security audits:**
   ```bash
   sudo apt install lynis
   sudo lynis audit system
   ```

5. **Monitor logs regularly:**
   ```bash
   sudo tail -f /var/log/auth.log
   ```

---

## WhatsApp Webhook Configuration

After deployment, configure your WhatsApp Business API:

1. Go to Meta Developer Console
2. Navigate to WhatsApp > Configuration
3. Set webhook URL: `https://your-domain.com/webhook`
4. Set verify token: (same as `WHATSAPP_VERIFY_TOKEN` in .env)
5. Subscribe to `messages` events

Test webhook:
```bash
curl -X GET 'https://your-domain.com/webhook?hub.mode=subscribe&hub.challenge=12345&hub.verify_token=your_verify_token'
```

---

## Support

For issues or questions:
- Check logs: `sudo journalctl -u agrosoko -f`
- Review application logs: `tail -f /var/log/agrosoko/error.log`
- Test API endpoints: Visit `https://your-domain.com/docs`

---

## Summary Checklist

- [ ] VPS provisioned and accessible
- [ ] Domain name configured (optional)
- [ ] System packages updated
- [ ] Application code deployed
- [ ] Python environment set up
- [ ] Environment variables configured
- [ ] Google credentials configured (if needed)
- [ ] Systemd service installed and running
- [ ] Nginx configured and running
- [ ] Firewall configured
- [ ] SSL certificate installed
- [ ] WhatsApp webhook configured
- [ ] Monitoring set up
- [ ] Backups configured

Your AgroGhala API should now be running consistently on your VPS! 🚀

