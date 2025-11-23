# AgroGhala VPS - Quick Reference Card

## 🚀 Quick Deploy

```bash
# 1. Upload files
rsync -avz --exclude 'venv' --exclude '__pycache__' ./ user@vps:/var/www/agrosoko.ai/

# 2. SSH and run setup
ssh user@vps
cd /var/www/agrosoko.ai
sudo bash deployment/setup.sh
```

---

## 📋 Essential Commands

### Service Management
```bash
sudo systemctl start agrosoko      # Start
sudo systemctl stop agrosoko       # Stop
sudo systemctl restart agrosoko    # Restart
sudo systemctl status agrosoko     # Status
```

### View Logs
```bash
sudo journalctl -u agrosoko -f                    # Service logs (live)
tail -f /var/log/agrosoko/error.log              # App error logs
tail -f /var/log/nginx/agrosoko_error.log        # Nginx logs
```

### Nginx
```bash
sudo nginx -t                      # Test config
sudo systemctl restart nginx       # Restart
sudo systemctl reload nginx        # Reload (no downtime)
```

---

## 🔍 Troubleshooting

### Service won't start?
```bash
sudo journalctl -u agrosoko -n 50 --no-pager     # Check logs
sudo netstat -tlnp | grep 8000                    # Check if port in use
ls -la /var/www/agrosoko.ai/.env                 # Check .env exists
```

### Fix permissions
```bash
sudo chown -R www-data:www-data /var/www/agrosoko.ai
sudo chmod 600 /var/www/agrosoko.ai/.env
```

### Test manually
```bash
cd /var/www/agrosoko.ai
sudo -u www-data ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🔄 Update Application

```bash
# From local machine
rsync -avz --exclude 'venv' --exclude '.env' ./ user@vps:/var/www/agrosoko.ai/

# On VPS
ssh user@vps
sudo systemctl restart agrosoko
```

---

## 🔐 SSL Setup

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
sudo certbot renew --dry-run  # Test auto-renewal
```

---

## 📊 Monitoring

```bash
# Check if running
sudo systemctl is-active agrosoko

# Check port
sudo netstat -tlnp | grep 8000

# System resources
free -h        # Memory
df -h          # Disk
top            # CPU
```

---

## 🧪 Test Endpoints

```bash
# Health check
curl http://localhost:8000

# Get counties
curl http://localhost:8000/api/counties

# Get weather
curl http://localhost:8000/api/weather/Nairobi

# Get prices
curl http://localhost:8000/api/prices

# API docs
curl http://localhost:8000/openapi.json
```

---

## 📝 File Locations

```
Application:     /var/www/agrosoko.ai/
Service file:    /etc/systemd/system/agrosoko.service
Nginx config:    /etc/nginx/sites-available/agrosoko
App logs:        /var/log/agrosoko/
Nginx logs:      /var/log/nginx/
Environment:     /var/www/agrosoko.ai/.env
Google creds:    /var/www/agrosoko.ai/credentials/google-creds.json
```

---

## 🔧 Configuration

### Edit .env
```bash
sudo nano /var/www/agrosoko.ai/.env
sudo systemctl restart agrosoko
```

### Edit nginx
```bash
sudo nano /etc/nginx/sites-available/agrosoko
sudo nginx -t
sudo systemctl reload nginx
```

### Edit systemd service
```bash
sudo nano /etc/systemd/system/agrosoko.service
sudo systemctl daemon-reload
sudo systemctl restart agrosoko
```

---

## 🛡️ Security

```bash
# Firewall status
sudo ufw status

# Allow port
sudo ufw allow 80/tcp

# Check SSL
sudo certbot certificates

# Update system
sudo apt update && sudo apt upgrade -y
```

---

## 💾 Backup

```bash
# Backup data
tar -czf ~/backup_$(date +%Y%m%d).tar.gz /var/www/agrosoko.ai/data/

# Backup .env
sudo cp /var/www/agrosoko.ai/.env ~/env_backup_$(date +%Y%m%d)
```

---

## 📱 WhatsApp Webhook

**URL:** `https://your-domain.com/webhook`
**Verify Token:** Set in `.env` as `WHATSAPP_VERIFY_TOKEN`

Test:
```bash
curl -X GET 'https://your-domain.com/webhook?hub.mode=subscribe&hub.challenge=12345&hub.verify_token=your_token'
```

---

## 🆘 Emergency

### App crashed?
```bash
sudo systemctl restart agrosoko
sudo journalctl -u agrosoko -n 100
```

### Nginx down?
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Out of disk?
```bash
df -h
sudo du -sh /var/log/*
sudo journalctl --vacuum-time=7d  # Clean old logs
```

### High CPU?
```bash
top
ps aux | grep uvicorn
sudo systemctl restart agrosoko
```

---

## 📞 Support Info

- API Docs: `https://your-domain.com/docs`
- Health: `https://your-domain.com/`
- OpenAPI: `https://your-domain.com/openapi.json`

