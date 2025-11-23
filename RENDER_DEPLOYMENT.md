# 🚀 Deploy AgroGhala to Render (CLI Guide)

## Prerequisites

- Git repository initialized and pushed to GitHub/GitLab
- Render account (sign up at https://render.com)
- Render CLI installed
- Terminal access

---

## Step 1: Install Render CLI

### macOS (using Homebrew)
```bash
brew tap render-oss/render
brew install render
```

### Linux/macOS (using curl)
```bash
curl -fsSL https://render.com/install-cli | sh
```

### Verify Installation
```bash
render version
```

---

## Step 2: Login to Render

```bash
# Login via browser
render login

# Or use API key
render config set-api-key <your-api-key>
```

**To get your API key:**
1. Go to https://dashboard.render.com/account/settings
2. Scroll to "API Keys"
3. Create new API key
4. Copy and use above

---

## Step 3: Initialize Git Repository (if not done)

```bash
cd /Users/ratego/Dev/agrosoko.ai

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AgroGhala API with buyer management"

# Add remote (GitHub example)
git remote add origin https://github.com/yourusername/agrosoko-ai.git

# Push to main branch
git push -u origin main
```

---

## Step 4: Deploy Using render.yaml (Recommended)

### A. Deploy from CLI

```bash
# Navigate to project directory
cd /Users/ratego/Dev/agrosoko.ai

# Create the service using render.yaml
render services create

# Or if you want to specify the blueprint
render blueprint launch
```

### B. Deploy from Dashboard (Alternative)

```bash
# Open dashboard
open https://dashboard.render.com

# Then:
# 1. Click "New +" → "Blueprint"
# 2. Connect your repository
# 3. Render will detect render.yaml automatically
# 4. Click "Apply"
```

---

## Step 5: Set Environment Variables

### Via CLI

```bash
# Set WhatsApp credentials (optional)
render services env set agrosoko-api WHATSAPP_TOKEN=your_token_here
render services env set agrosoko-api WHATSAPP_PHONE_ID=your_phone_id
render services env set agrosoko-api WHATSAPP_VERIFY_TOKEN=your_verify_token

# Set Google Sheets credentials (optional)
render services env set agrosoko-api GOOGLE_SHEETS_CREDS_PATH=/etc/secrets/google-creds.json

# Set OpenWeather API key (optional)
render services env set agrosoko-api OPENWEATHER_API_KEY=your_key
```

### Via Dashboard (Easier for First Time)

1. Go to https://dashboard.render.com
2. Click on your service "agrosoko-api"
3. Go to "Environment" tab
4. Add environment variables:
   - `WHATSAPP_TOKEN` (optional)
   - `WHATSAPP_PHONE_ID` (optional)
   - `WHATSAPP_VERIFY_TOKEN` (optional)
   - `GOOGLE_SHEETS_CREDS_PATH` (optional)
   - `OPENWEATHER_API_KEY` (optional)

**Note:** The API works without these credentials. They're only needed for:
- WhatsApp notifications
- Google Sheets logging
- OpenWeatherMap backup (Open-Meteo works without API key)

---

## Step 6: Monitor Deployment

### Via CLI

```bash
# Get service status
render services list

# View logs
render logs --service agrosoko-api --tail

# Get service details
render services get agrosoko-api
```

### Via Dashboard

```bash
# Open service logs
open https://dashboard.render.com/select/services
```

---

## Step 7: Test Your Deployment

### Get Your Service URL

```bash
# Get service URL
render services get agrosoko-api | grep "URL"
```

Or find it in the dashboard at: `https://dashboard.render.com`

### Test the API

```bash
# Replace with your actual Render URL
export RENDER_URL="https://agrosoko-api.onrender.com"

# Test root endpoint
curl $RENDER_URL/

# Test prices endpoint
curl $RENDER_URL/api/prices/fair

# Test weather endpoint
curl $RENDER_URL/api/weather/Nairobi

# Test buyers endpoint (NEW!)
curl "$RENDER_URL/api/buyers/by-commodity?county=Nairobi"

# Test all endpoints
curl $RENDER_URL/docs
```

---

## Step 8: Configure Custom Domain (Optional)

### Via CLI

```bash
# Add custom domain
render domains create agrosoko-api yourdomain.com

# View domains
render domains list agrosoko-api
```

### Via Dashboard

1. Go to service settings
2. Click "Custom Domains"
3. Add your domain
4. Follow DNS configuration instructions

---

## Quick Deployment Commands

### One-Line Deploy

```bash
cd /Users/ratego/Dev/agrosoko.ai && \
git add . && \
git commit -m "Update" && \
git push && \
render services redeploy agrosoko-api
```

### Force Redeploy

```bash
render services redeploy agrosoko-api --clear-cache
```

### View Real-Time Logs

```bash
render logs --service agrosoko-api --tail --follow
```

---

## Render.yaml Configuration

Your `render.yaml` is already configured with:

```yaml
services:
  - type: web
    name: agrosoko-api
    runtime: python
    region: oregon
    plan: free
    branch: main
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /
    autoDeploy: true
```

### Key Settings:

- **Free Plan**: No credit card required for basic usage
- **Auto Deploy**: Deploys automatically on git push
- **Health Check**: Monitors `/` endpoint
- **Region**: Oregon (change to `frankfurt` for Europe, `singapore` for Asia)

---

## Environment Variables Needed

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `WHATSAPP_TOKEN` | Optional | WhatsApp Cloud API token |
| `WHATSAPP_PHONE_ID` | Optional | WhatsApp phone number ID |
| `WHATSAPP_VERIFY_TOKEN` | Optional | Webhook verification |
| `GOOGLE_SHEETS_CREDS_PATH` | Optional | Google Sheets logging |
| `OPENWEATHER_API_KEY` | Optional | Weather backup API |

**Note:** All features work without credentials except WhatsApp messaging and Google Sheets logging.

---

## Troubleshooting

### Issue: Build Fails

```bash
# Check build logs
render logs --service agrosoko-api --build

# Common fixes:
# 1. Verify requirements.txt is correct
# 2. Check Python version compatibility
# 3. Ensure all imports are available
```

### Issue: Service Won't Start

```bash
# Check runtime logs
render logs --service agrosoko-api --tail

# Common fixes:
# 1. Verify startCommand in render.yaml
# 2. Check PORT environment variable usage
# 3. Ensure app.main:app is correct path
```

### Issue: Health Check Failing

```bash
# Test health check endpoint locally
curl https://your-app.onrender.com/

# Should return:
# {"status": "AgroGhala Agentic API is running", ...}
```

### Issue: Slow Cold Starts

**On Free Plan**: Services spin down after 15 minutes of inactivity.

**Solutions:**
1. Upgrade to paid plan ($7/month) for always-on
2. Use external uptime monitor (UptimeRobot, etc.)
3. Accept 30-60 second cold start delay

---

## Advanced CLI Commands

### Service Management

```bash
# List all services
render services list

# Get service details
render services get agrosoko-api

# Delete service
render services delete agrosoko-api

# Suspend service
render services suspend agrosoko-api

# Resume service
render services resume agrosoko-api
```

### Environment Variables

```bash
# List all env vars
render services env list agrosoko-api

# Get specific env var
render services env get agrosoko-api WHATSAPP_TOKEN

# Delete env var
render services env unset agrosoko-api OLD_VAR_NAME
```

### Logs

```bash
# View build logs
render logs --service agrosoko-api --build

# View runtime logs
render logs --service agrosoko-api --tail

# Follow logs in real-time
render logs --service agrosoko-api --tail --follow

# Filter logs
render logs --service agrosoko-api --tail | grep "ERROR"
```

---

## Production Checklist

Before going live:

- [ ] Git repository pushed to GitHub/GitLab
- [ ] Render CLI installed and authenticated
- [ ] render.yaml configured
- [ ] Environment variables set (if needed)
- [ ] Service deployed successfully
- [ ] Health check passing
- [ ] All endpoints tested
- [ ] API documentation accessible at `/docs`
- [ ] WhatsApp webhook configured (if using)
- [ ] Custom domain configured (if needed)
- [ ] SSL certificate active (automatic on Render)
- [ ] Monitoring set up
- [ ] Backup plan for data files

---

## Cost Estimate

### Free Tier
- ✅ 750 hours/month
- ✅ Automatic SSL
- ✅ Built from GitHub/GitLab
- ⚠️ Spins down after 15 min inactivity
- ⚠️ 100GB bandwidth/month

### Starter Plan ($7/month)
- ✅ Always on
- ✅ 400GB bandwidth/month
- ✅ Better performance
- ✅ No cold starts

**Recommendation**: Start with Free, upgrade if needed.

---

## Update Workflow

### Standard Update

```bash
# Make changes to code
# ...

# Commit and push
git add .
git commit -m "Your update message"
git push

# Render auto-deploys on push ✅
```

### Manual Redeploy

```bash
# Trigger manual deployment
render services redeploy agrosoko-api

# With cache clear
render services redeploy agrosoko-api --clear-cache
```

---

## Monitoring & Alerts

### Via CLI

```bash
# Check service health
render services get agrosoko-api | grep "status"

# Monitor logs
render logs --service agrosoko-api --tail --follow
```

### Via Dashboard

1. Go to https://dashboard.render.com
2. Select your service
3. Check "Events" tab for deployment history
4. Check "Metrics" for performance data

### Set Up Alerts

1. Go to service settings
2. Click "Notifications"
3. Add email/Slack webhooks
4. Configure alert triggers

---

## Next Steps After Deployment

1. **Test All Endpoints**
   ```bash
   curl https://your-app.onrender.com/api/prices/fair
   curl https://your-app.onrender.com/api/weather/Nairobi
   curl https://your-app.onrender.com/api/buyers/by-commodity?county=Nairobi
   ```

2. **Update Orchestrate**
   - Replace localhost URLs with your Render URL
   - Test conversation flow
   - Verify API responses

3. **Configure WhatsApp Webhook**
   - Update webhook URL to `https://your-app.onrender.com/webhook`
   - Test message flow

4. **Monitor Performance**
   - Watch logs for errors
   - Check response times
   - Monitor bandwidth usage

5. **Set Up Backups**
   - Export buyer data regularly
   - Backup environment variables
   - Document configuration

---

## Support & Resources

**Render CLI Documentation**: https://render.com/docs/cli  
**Render Dashboard**: https://dashboard.render.com  
**Render Status**: https://status.render.com  
**Render Community**: https://community.render.com

**AgroGhala API Docs**: https://your-app.onrender.com/docs  
**This Guide**: RENDER_DEPLOYMENT.md

---

## Quick Reference

```bash
# Login
render login

# Deploy
render blueprint launch

# Check status
render services list

# View logs
render logs --service agrosoko-api --tail --follow

# Redeploy
render services redeploy agrosoko-api

# Set env var
render services env set agrosoko-api KEY=value

# Get service URL
render services get agrosoko-api | grep URL
```

---

**Status**: Ready to Deploy ✅  
**Time to Deploy**: 5-10 minutes  
**Cost**: Free tier available  
**Auto Deploy**: Enabled on git push

🚀 **Let's deploy your AgroGhala API!**

