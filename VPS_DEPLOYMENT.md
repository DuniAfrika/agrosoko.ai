# AgroGhala VPS Deployment

Complete production deployment package for running AgroGhala API consistently on a Linux VPS.

## 🎯 What This Includes

Your application now has everything needed for a production VPS deployment:

✅ **Systemd Service** - Auto-start, auto-restart, process management  
✅ **Nginx Configuration** - Reverse proxy, SSL, rate limiting, security headers  
✅ **Automated Setup Script** - One-command deployment  
✅ **Health Check Script** - Verify deployment status  
✅ **Complete Documentation** - Step-by-step guides and troubleshooting  
✅ **Quick Reference** - Command cheat sheet for daily operations  

## 📁 Deployment Files

All files are in the `deployment/` directory:

```
deployment/
├── README.md                  # Deployment overview
├── DEPLOYMENT_GUIDE.md        # Complete step-by-step guide (⭐ main guide)
├── QUICK_REFERENCE.md         # Command cheat sheet
├── agrosoko.service           # Systemd service file
├── nginx.conf                 # Nginx configuration
├── setup.sh                   # Automated setup script
└── health-check.sh            # Health check script
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# From your local machine - upload files
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' \
  /Users/ratego/Dev/agrosoko.ai/ user@your-vps:/var/www/agrosoko.ai/

# On your VPS - run setup
ssh user@your-vps
cd /var/www/agrosoko.ai
sudo bash deployment/setup.sh
```

The script will:
- Install all dependencies (Python, Nginx, Certbot)
- Set up Python virtual environment
- Configure systemd service
- Configure Nginx reverse proxy
- Set up firewall
- Start services

### Option 2: Manual Setup

See **[deployment/DEPLOYMENT_GUIDE.md](deployment/DEPLOYMENT_GUIDE.md)** for detailed manual steps.

## 📋 Prerequisites

**On your VPS:**
- Ubuntu 20.04+, Debian 11+, or similar Linux distribution
- Root or sudo access
- At least 1GB RAM (2GB recommended)
- 20GB disk space

**Optional (but recommended):**
- Domain name pointed to your VPS IP
- SSL certificate (can be set up with Let's Encrypt)

## 🔧 Configuration

### 1. Update Domain Name

Before deployment, update the domain in:
- `deployment/nginx.conf` - Replace `your-domain.com`
- `deployment/setup.sh` - Replace `your-domain.com`

### 2. Environment Variables

On your VPS, create `/var/www/agrosoko.ai/.env`:

```env
# WhatsApp Configuration
WHATSAPP_TOKEN=your_whatsapp_token_here
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

### 3. Google Credentials (if using Sheets)

Upload your service account JSON:
```bash
scp google-creds.json user@vps:/var/www/agrosoko.ai/credentials/
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   Internet                      │
└────────────────────┬────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │   Nginx (Port 80/443)   │
        │   - SSL/TLS             │
        │   - Rate Limiting       │
        │   - Security Headers    │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │  Uvicorn (Port 8000)    │
        │  - 4 Workers            │
        │  - Load Balanced        │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   FastAPI Application   │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────────────────┐
        │          Services                   │
        │  - KAMIS Scraper                    │
        │  - Weather API                      │
        │  - Price Engine                     │
        │  - WhatsApp Agent                   │
        │  - Google Sheets Logger             │
        │  - Buyers Service                   │
        └─────────────────────────────────────┘
```

## 📊 What Happens After Deployment

### Systemd Service
- **Auto-start** on boot
- **Auto-restart** on failure (10 second delay)
- Runs as `www-data` user (security)
- Logs to `/var/log/agrosoko/`

### Nginx
- Handles all incoming web traffic
- SSL/TLS termination (HTTPS)
- Rate limiting (10 req/s for API, 20 req/s for webhooks)
- Security headers
- Static file serving
- Reverse proxy to Uvicorn

### Application
- Runs 4 worker processes (high availability)
- Accessible at `http://your-domain.com`
- API docs at `http://your-domain.com/docs`
- Webhook at `http://your-domain.com/webhook`

## 🔍 Verification

### Run Health Check

```bash
# On your VPS
cd /var/www/agrosoko.ai
sudo bash deployment/health-check.sh
```

This checks:
- ✓ Systemd service running
- ✓ Application process alive
- ✓ Port 8000 listening
- ✓ API endpoints responding
- ✓ Nginx running
- ✓ Configuration valid
- ✓ Files and directories present
- ✓ Firewall configured

### Manual Verification

```bash
# Check service
sudo systemctl status agrosoko

# Test API locally
curl http://localhost:8000

# Test API externally
curl http://your-domain.com

# View logs
sudo journalctl -u agrosoko -f
```

## 🛠️ Daily Operations

### Service Management

```bash
# Start
sudo systemctl start agrosoko

# Stop
sudo systemctl stop agrosoko

# Restart
sudo systemctl restart agrosoko

# Status
sudo systemctl status agrosoko

# View logs
sudo journalctl -u agrosoko -f
```

### Update Application

```bash
# From local machine
rsync -avz --exclude 'venv' --exclude '.env' \
  /Users/ratego/Dev/agrosoko.ai/ user@vps:/var/www/agrosoko.ai/

# On VPS
ssh user@vps
sudo systemctl restart agrosoko
```

### Update Configuration

```bash
# Edit environment
sudo nano /var/www/agrosoko.ai/.env
sudo systemctl restart agrosoko

# Edit nginx
sudo nano /etc/nginx/sites-available/agrosoko
sudo nginx -t
sudo systemctl reload nginx

# Edit systemd service
sudo nano /etc/systemd/system/agrosoko.service
sudo systemctl daemon-reload
sudo systemctl restart agrosoko
```

## 🔐 SSL Setup (HTTPS)

After basic deployment, enable SSL:

```bash
# Install certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Uncomment HTTPS block in nginx config
sudo nano /etc/nginx/sites-available/agrosoko
# Uncomment the server block for port 443

# Reload nginx
sudo systemctl reload nginx

# Test auto-renewal
sudo certbot renew --dry-run
```

## 📱 WhatsApp Webhook Configuration

After deployment:

1. Go to Meta Developer Console
2. Navigate to WhatsApp > Configuration
3. Set webhook URL: `https://your-domain.com/webhook`
4. Set verify token: (from `.env` file)
5. Subscribe to `messages` events

Test:
```bash
curl -X GET 'https://your-domain.com/webhook?hub.mode=subscribe&hub.challenge=12345&hub.verify_token=your_verify_token'
```

## 📈 Monitoring

### Check System Health
```bash
# Service status
sudo systemctl is-active agrosoko

# Resource usage
free -h              # Memory
df -h                # Disk
top                  # CPU & processes

# Port listening
sudo netstat -tlnp | grep 8000
```

### View Logs
```bash
# Application logs (systemd)
sudo journalctl -u agrosoko -f

# Application error logs
tail -f /var/log/agrosoko/error.log

# Application access logs
tail -f /var/log/agrosoko/access.log

# Nginx logs
tail -f /var/log/nginx/agrosoko_access.log
tail -f /var/log/nginx/agrosoko_error.log
```

## 🔧 Troubleshooting

### Service Won't Start

```bash
# Check detailed logs
sudo journalctl -u agrosoko -n 50 --no-pager

# Check if port in use
sudo netstat -tlnp | grep 8000

# Check permissions
ls -la /var/www/agrosoko.ai/

# Check .env exists
sudo cat /var/www/agrosoko.ai/.env

# Test manually
cd /var/www/agrosoko.ai
sudo -u www-data ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Fix Common Issues

```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/agrosoko.ai
sudo chmod 600 /var/www/agrosoko.ai/.env

# Reinstall dependencies
cd /var/www/agrosoko.ai
sudo -u www-data ./venv/bin/pip install --force-reinstall -r requirements.txt

# Restart everything
sudo systemctl restart agrosoko
sudo systemctl restart nginx
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [deployment/DEPLOYMENT_GUIDE.md](deployment/DEPLOYMENT_GUIDE.md) | Complete step-by-step manual setup |
| [deployment/QUICK_REFERENCE.md](deployment/QUICK_REFERENCE.md) | Quick command reference card |
| [deployment/README.md](deployment/README.md) | Deployment files overview |
| This file (VPS_DEPLOYMENT.md) | Main deployment overview |

## 💡 Tips

1. **Keep backups** of your `.env` and `data/` directory
2. **Monitor logs** regularly: `sudo journalctl -u agrosoko -f`
3. **Update system** regularly: `sudo apt update && sudo apt upgrade`
4. **Use SSL** for production (Let's Encrypt is free)
5. **Set up monitoring** (e.g., UptimeRobot, Pingdom)
6. **Configure log rotation** (included in setup script)

## 🆘 Getting Help

**First steps:**
1. Run health check: `sudo bash deployment/health-check.sh`
2. Check logs: `sudo journalctl -u agrosoko -f`
3. Check nginx: `sudo nginx -t`
4. Review [deployment/DEPLOYMENT_GUIDE.md](deployment/DEPLOYMENT_GUIDE.md)

**API Documentation:**
- Interactive docs: `https://your-domain.com/docs`
- OpenAPI spec: `https://your-domain.com/openapi.json`
- ReDoc: `https://your-domain.com/redoc`

## ✅ Post-Deployment Checklist

- [ ] Files uploaded to VPS
- [ ] Setup script completed successfully
- [ ] Service running: `sudo systemctl status agrosoko`
- [ ] Nginx running: `sudo systemctl status nginx`
- [ ] API responding: `curl http://localhost:8000`
- [ ] Domain configured (if using)
- [ ] SSL certificate installed (if using domain)
- [ ] Environment variables set in `.env`
- [ ] Google credentials uploaded (if using Sheets)
- [ ] WhatsApp webhook configured
- [ ] Firewall enabled: `sudo ufw status`
- [ ] Health check passing: `sudo bash deployment/health-check.sh`
- [ ] Tested all API endpoints
- [ ] Monitoring set up
- [ ] Backup strategy in place

## 🎉 Success!

Your AgroGhala API is now running professionally on your VPS with:
- ✅ Automatic startup on boot
- ✅ Automatic restart on failures
- ✅ Production-grade reverse proxy
- ✅ SSL/HTTPS support
- ✅ Security hardening
- ✅ Comprehensive logging
- ✅ Easy management commands

**Your API is now accessible at:**
- `http://your-domain.com` (or `http://your-vps-ip`)
- `https://your-domain.com` (after SSL setup)
- API Docs: `https://your-domain.com/docs`

**Next steps:**
1. Test all endpoints using the API docs
2. Configure WhatsApp webhook
3. Set up monitoring/alerts
4. Create backup strategy
5. Document your deployment specifics

Happy farming! 🌾🚀

