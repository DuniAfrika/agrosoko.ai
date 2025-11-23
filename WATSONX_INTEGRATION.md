# watsonx Orchestrate Integration Guide

## Overview

The AgroGhala API is now ready for integration with watsonx Orchestrate using the OpenAPI specification.

## Files Generated

- **`openapi.json`** - OpenAPI 3.0 specification file for watsonx Orchestrate

## Available Endpoints in OpenAPI Spec

1. **`GET /`** - API status and endpoints list
2. **`GET /api/scrape/kamis`** - Scrape KAMIS market data
3. **`GET /api/weather/{county}`** - Get weather for Kenyan county
4. **`GET /api/prices`** - Get wholesale prices
5. **`GET /api/prices/fair`** - Get fair farm-gate prices
6. **`GET /api/counties`** - Get all 47 Kenyan counties
7. **`POST /trigger-daily`** - Trigger daily workflow
8. **`POST /webhook`** - WhatsApp webhook endpoint

## How to Import into watsonx Orchestrate

### Step 1: Get the OpenAPI File

The file `openapi.json` is already generated in your project root.

You can also download it from a running server:
```bash
curl http://localhost:8000/openapi.json > openapi.json
```

### Step 2: Import into watsonx Orchestrate

1. Log in to **watsonx Orchestrate**
2. Go to **Skills** or **APIs** section
3. Click **"Add API"** or **"Import OpenAPI"**
4. Upload the `openapi.json` file
5. Give it a name: **"AgroGhala API"**

### Step 3: Configure Server URL

In watsonx Orchestrate settings for this API:

**For Development:**
```
http://localhost:8000
```

**For Production:**
```
https://your-domain.com
```

**Using ngrok (for testing):**
```bash
# Start ngrok
ngrok http 8000

# Use the generated URL (e.g., https://abc123.ngrok.io)
https://abc123.ngrok.io
```

### Step 4: Test the Integration

In watsonx Orchestrate, test these skills:

1. **Get KAMIS Prices**
   - Skill: `GET /api/scrape/kamis`
   - No parameters needed
   - Returns: Current market prices

2. **Get Weather**
   - Skill: `GET /api/weather/{county}`
   - Parameter: `county` = "Nairobi"
   - Returns: Weather forecast

3. **Get Fair Prices**
   - Skill: `GET /api/prices/fair`
   - No parameters needed
   - Returns: Calculated farm-gate prices

## Example Workflows in watsonx Orchestrate

### Workflow 1: Daily Price Update

```
1. Call "Get KAMIS Prices" skill
2. Call "Get Fair Prices" skill
3. Store results in variable
4. Send notification (using other watsonx skills)
```

### Workflow 2: Weather-Based Advisory

```
1. Call "Get Counties" skill
2. For each county:
   a. Call "Get Weather" with county name
   b. If rainfall > 70%:
      - Generate warning message
      - Send to farmers in that county
```

### Workflow 3: Complete Farmer Notification

```
1. Call "Get KAMIS Prices" skill
2. Call "Get Weather" for farmer's county
3. Call "Get Fair Prices" skill
4. Combine data into message
5. Send via WhatsApp or other channel
```

## Authentication

Currently, the API does **not require authentication** for read endpoints.

For production, you may want to add:
- API keys
- OAuth2
- JWT tokens

Update the OpenAPI spec accordingly if adding authentication.

## Regenerating OpenAPI Spec

If you modify the API endpoints, regenerate the spec:

```bash
# Method 1: Use the export script
python export_openapi.py

# Method 2: Download from running server
curl http://localhost:8000/openapi.json > openapi.json

# Method 3: Access in browser
# Visit: http://localhost:8000/openapi.json
```

## Testing Before Import

Before importing to watsonx Orchestrate, test the API:

```bash
# Start the server
./run.sh

# Test endpoints
curl http://localhost:8000/api/scrape/kamis
curl http://localhost:8000/api/weather/Nairobi
curl http://localhost:8000/api/prices/fair

# View interactive docs
open http://localhost:8000/docs
```

## Troubleshooting

### Issue: watsonx can't reach the API

**Solution 1: Use ngrok**
```bash
ngrok http 8000
# Use the ngrok URL in watsonx
```

**Solution 2: Deploy to cloud**
- Deploy to Heroku, AWS, or Azure
- Use the public URL in watsonx

### Issue: OpenAPI import fails

**Check:**
1. File is valid JSON: `cat openapi.json | jq`
2. OpenAPI version is supported (3.0+)
3. All endpoints have proper descriptions

**Fix:**
```bash
# Regenerate the file
python export_openapi.py
```

### Issue: Endpoints not showing in watsonx

**Verify:**
1. Server is running: `curl http://localhost:8000/`
2. Endpoints are accessible: `curl http://localhost:8000/api/prices`
3. OpenAPI spec is up-to-date

## Production Considerations

### Security
- Add API authentication
- Rate limiting
- CORS configuration
- HTTPS required

### Reliability
- Deploy to production server
- Use load balancer
- Add monitoring
- Set up logging

### Scalability
- Cache API responses
- Use CDN for static content
- Database for logging (instead of just Google Sheets)

## Support

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- API Guide: `API.md`

### Files
- `openapi.json` - OpenAPI specification
- `export_openapi.py` - Script to regenerate spec
- `workflow.json` - Sample workflow configuration

---

**Ready to use!** Import `openapi.json` into watsonx Orchestrate and start building workflows! 🚀

