# Deployment Files

This directory contains all necessary files for deploying AgroGhala API to a Linux VPS.

## Files

- **`agrosoko.service`** - Systemd service configuration
- **`nginx.conf`** - Nginx reverse proxy configuration
- **`setup.sh`** - Automated deployment script
- **`DEPLOYMENT_GUIDE.md`** - Complete step-by-step deployment guide
- **`QUICK_REFERENCE.md`** - Quick command reference card

## Quick Start

### Automated Deployment

```bash
# 1. Copy files to VPS
rsync -avz --exclude 'venv' --exclude '__pycache__' ./ user@your-vps:/var/www/agrosoko.ai/

# 2. Run setup script
ssh user@your-vps
cd /var/www/agrosoko.ai
sudo bash deployment/setup.sh
```

### Manual Deployment

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for detailed instructions.

## What Gets Installed

- **Python 3.11** virtual environment
- **Systemd service** for automatic startup and management
- **Nginx** as reverse proxy
- **Certbot** for SSL certificates
- **UFW firewall** configuration
- **Log rotation** setup

## Architecture

```
Internet
   ↓
Nginx (Port 80/443)
   ↓
Uvicorn (Port 8000)
   ↓
FastAPI Application
   ↓
Services (KAMIS, Weather, Sheets, WhatsApp)
```

## Security Features

- ✅ HTTPS with Let's Encrypt SSL
- ✅ Rate limiting on API endpoints
- ✅ Firewall configuration
- ✅ Restricted file permissions
- ✅ Service isolation with systemd
- ✅ Log rotation

## Monitoring

### Service Status
```bash
sudo systemctl status agrosoko
```

### View Logs
```bash
# Application logs
sudo journalctl -u agrosoko -f

# Error logs
tail -f /var/log/agrosoko/error.log

# Nginx logs
tail -f /var/log/nginx/agrosoko_error.log
```

### Health Check
```bash
curl http://localhost:8000
```

## Configuration

### Environment Variables

Create `/var/www/agrosoko.ai/.env`:

```env
WHATSAPP_TOKEN=your_token
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=your_verify_token
GOOGLE_SHEETS_CREDS_PATH=/var/www/agrosoko.ai/credentials/google-creds.json
OPENWEATHER_API_KEY=your_key
ENVIRONMENT=production
```

### Systemd Service

Location: `/etc/systemd/system/agrosoko.service`

Key settings:
- Runs as `www-data` user
- Auto-restarts on failure
- 4 workers for high availability
- Logs to `/var/log/agrosoko/`

### Nginx

Location: `/etc/nginx/sites-available/agrosoko`

Features:
- Reverse proxy to Uvicorn
- SSL/TLS configuration
- Rate limiting
- Security headers
- Static file serving
- Health check endpoint

## Maintenance

### Update Application
```bash
rsync -avz --exclude 'venv' --exclude '.env' ./ user@vps:/var/www/agrosoko.ai/
ssh user@vps 'sudo systemctl restart agrosoko'
```

### Update Dependencies
```bash
ssh user@vps
cd /var/www/agrosoko.ai
sudo -u www-data ./venv/bin/pip install -r requirements.txt
sudo systemctl restart agrosoko
```

### Renew SSL Certificate
```bash
sudo certbot renew
# Auto-renewal is configured in cron
```

## Troubleshooting

### Service Won't Start
1. Check logs: `sudo journalctl -u agrosoko -n 50`
2. Check permissions: `ls -la /var/www/agrosoko.ai/`
3. Check .env file: `sudo cat /var/www/agrosoko.ai/.env`
4. Test manually: `cd /var/www/agrosoko.ai && sudo -u www-data ./venv/bin/uvicorn app.main:app`

### Port Already in Use
```bash
sudo netstat -tlnp | grep 8000
sudo kill <PID>
sudo systemctl restart agrosoko
```

### Permission Errors
```bash
sudo chown -R www-data:www-data /var/www/agrosoko.ai
sudo chmod 600 /var/www/agrosoko.ai/.env
```

## Performance

### Recommended VPS Specs

**Minimum:**
- 1 vCPU
- 1GB RAM
- 20GB SSD

**Recommended:**
- 2 vCPU
- 2GB RAM
- 40GB SSD

### Worker Configuration

Default: 4 workers

Adjust in `/etc/systemd/system/agrosoko.service`:
```ini
ExecStart=/var/www/agrosoko.ai/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Formula: `(2 × CPU cores) + 1`

## Backup

Recommended backup strategy:
- Daily backup of `/var/www/agrosoko.ai/data/`
- Weekly backup of `.env` and credentials
- Keep 7 days of backups

## Support

For issues:
1. Check logs
2. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
4. Test API: `https://your-domain.com/docs`

## Links

- [Full Deployment Guide](DEPLOYMENT_GUIDE.md) - Complete setup instructions
- [Quick Reference](QUICK_REFERENCE.md) - Command cheat sheet
- [Main README](../README.md) - Application documentation
- [API Documentation](../API.md) - API endpoints reference

