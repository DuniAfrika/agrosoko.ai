# AgroGhala Agentic MVP

This project implements the AgroGhala Agentic workflow for daily farm-gate price automation.

## Key Features

✅ **Real-Time Weather Data**: Integrated with Open-Meteo API providing accurate weather forecasts for all 47 Kenyan counties
✅ **Automated Price Scraping**: Daily scraping of wholesale prices from KAMIS with intelligent caching
✅ **Fair Price Calculation**: Intelligent farm-gate price calculation based on market data
✅ **WhatsApp Integration**: Automated farmer notifications via WhatsApp Cloud API
✅ **Buyer Directory**: 20+ verified buyers (Hotels, Restaurants, Mama Mbogas, Supermarkets, Wholesalers)
✅ **Buyer Matching**: Connect farmers with buyers based on crop, location, and buyer type
✅ **Organized Buyer Display**: 2 buyers per commodity (Tomatoes, Sukuma, Onions, Cabbage) - clean, mobile-friendly format
✅ **Activity Logging**: Complete audit trail in Google Sheets
✅ **Multi-Tier API Fallback**: Reliable weather data with automatic fallback systems

## Modules

- **kamis_scraper.py**: Intelligent KAMIS data scraper with smart caching. **First run**: Downloads 3000 historical rows per commodity (18,000 total). **Daily runs**: Fetches only today's data for efficiency. **Smart caching**: Returns cached data if already scraped today. Extracts real Nairobi wholesale prices for Tomatoes, Sukuma, Onions, Cabbage, Maize, and Beans. Saves all data to Excel in `data/` folder.
- **buyers_service.py**: Buyer directory management. Manages 20+ verified buyers from Excel database. Supports filtering by buyer type, county, and crop interest. Provides statistics on buyer capacity and distribution.
- **write_excel.py**: Saves prices to `/data/prices.xlsx`.
- **weather_api.py**: Fetches real weather data from Open-Meteo API (free, no API key required) with OpenWeatherMap fallback.
- **price_engine.py**: Calculates fair farm-gate prices.
- **sheets_logger.py**: Comprehensive Google Sheets integration. Automatically creates spreadsheet with Activity_Log, Farmers, and Buyers worksheets. Logs all farmer interactions, manages farmer database, and tracks buyers by crop. Includes mock data fallback when offline. Requires Google Cloud service account setup.
- **whatsapp_agent.py**: Sends messages via WhatsApp Cloud API.
- **app/main.py**: FastAPI application to handle webhooks and trigger workflows.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn requests pandas openpyxl beautifulsoup4 gspread oauth2client google-auth
   ```

2. **Run the Server**:
   ```bash
   ./run.sh
   ```
   
   That's it! The server will start at http://localhost:8000

## Features Available Without Credentials

- ✅ KAMIS price scraping (18,000+ rows of real market data with smart caching)
- ✅ Weather forecasts (all 47 Kenyan counties)
- ✅ Price calculations
- ✅ Buyer directory (20+ verified buyers)
- ✅ Excel data exports
- ✅ Full API endpoints

## Full Setup (Optional)

1. **Environment Variables** (Optional):
   ```bash
   # Optional: Copy template if you want to configure credentials
   cp env.example .env
   nano .env
   ```
   
   **For full functionality, configure**:
   - `GOOGLE_SHEETS_CREDS_PATH`: Google Service Account JSON (for logging)
   - `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `WHATSAPP_VERIFY_TOKEN`: WhatsApp API (for messaging)
   - `OPENWEATHER_API_KEY`: OpenWeatherMap (optional backup weather)

2. **Configure WhatsApp Webhook**:
   - **Production URL**: `https://agrosoko.keverd.com/webhook`
   - **Development URL** (for testing): Use ngrok - `ngrok http 8000` then `https://<ngrok-url>/webhook`
   - Verify Token: Match with `WHATSAPP_VERIFY_TOKEN`

4. **Configure watsonx Orchestrate** (optional):
   - Import `workflow.json`
   - Update the URL to your deployed API endpoint

## API Endpoints

Once running, access these endpoints:

**Market Data & Weather:**
- **Scrape KAMIS**: `GET /api/scrape/kamis` - Get latest market prices (with smart caching)
- **Weather Data**: `GET /api/weather/{county}` - Get weather for any county
- **Wholesale Prices**: `GET /api/prices` - Get current wholesale prices
- **Fair Prices**: `GET /api/prices/fair` - Get calculated farm-gate prices
- **Counties List**: `GET /api/counties` - Get all 47 Kenyan counties

**Buyer Directory:**
- **Buyers by Commodity**: `GET /api/buyers/by-commodity?county=Nairobi` - **NEW!** Get 2 buyers per commodity (organized & mobile-friendly)
- **All Buyers**: `GET /api/buyers` - Get all buyers (filter by type, county, or crop)
- **Buyer Details**: `GET /api/buyers/{buyer_id}` - Get specific buyer information
- **Buyer Stats**: `GET /api/buyers/stats` - Get buyer statistics and capacity
- **Buyer Types**: `GET /api/buyers/types` - Get list of buyer categories

**Full API Documentation**: See [API.md](API.md)

**Interactive Docs**: 
- Production: `https://agrosoko.keverd.com/docs`
- Development: `http://localhost:8000/docs`

**OpenAPI Spec**: 
- Production: `https://agrosoko.keverd.com/openapi.json`
- Development: `http://localhost:8000/openapi.json`

**watsonx Orchestrate**: See [WATSONX_INTEGRATION.md](WATSONX_INTEGRATION.md) for integration guide

## 🤖 Agent Guidelines & Implementation

**New to implementing the agent?** Start here: **[IMPLEMENTATION_INDEX.md](IMPLEMENTATION_INDEX.md)** 🚀

Complete documentation for setting up conversational agents (Orchestrate, watsonx Assistant, or similar):

### 📚 Documentation Package
- **[IMPLEMENTATION_INDEX.md](IMPLEMENTATION_INDEX.md)** - 🎯 **START HERE** - Navigation guide for all documentation
- **[GUIDELINES_SUMMARY.md](GUIDELINES_SUMMARY.md)** - Overview and quick start paths
- **[AGENT_GUIDELINE.md](AGENT_GUIDELINE.md)** - Comprehensive guide (70+ pages)
- **[ORCHESTRATE_GUIDELINE.md](ORCHESTRATE_GUIDELINE.md)** - Platform-specific structured format
- **[ORCHESTRATE_CONFIG.txt](ORCHESTRATE_CONFIG.txt)** - Copy-paste ready configuration (fastest setup!)
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick lookup card for daily use
- **[CONVERSATION_FLOW.md](CONVERSATION_FLOW.md)** - Visual flow diagrams and logic

### 🎬 Quick Start Options

**Option 1: Orchestrate (30 minutes)**
1. Open [ORCHESTRATE_CONFIG.txt](ORCHESTRATE_CONFIG.txt)
2. Copy-paste 8 guidelines into Orchestrate
3. Update API URL
4. Test and deploy ✅

**Option 2: Other Platform (2-3 hours)**
- Follow the learning path in [IMPLEMENTATION_INDEX.md](IMPLEMENTATION_INDEX.md)

**Option 3: Custom Development (4-8 hours)**
- Full specs in [AGENT_GUIDELINE.md](AGENT_GUIDELINE.md)

### 💬 Conversation Flow

```
User: "join agrosoko"
  → Bot: Welcome message

User: "start Nairobi"
  → Bot: Farm-gate prices + rain forecast + "Do you have produce?"
       [Calls: /api/prices/fair + /api/weather/Nairobi]

User: "YES"
  → Bot: List of verified buyers with contacts
       [Calls: /api/buyers?county=Nairobi]
```

**Error Handling**: All other inputs receive clear error messages with guidance.

### ✅ 8 Core Guidelines
1. Sandbox Join (`join <word>`)
2. Price & Weather Request (`start {county}`)
3. Buyer List Response (`YES`)
4. Invalid County Error
5. Invalid Response Error
6. Invalid Command Help
7. API Error Handler
8. Support Request Handler

## Workflow

1. **Daily Trigger (4:30 AM)**: Orchestrate calls `/trigger-daily`.
2. **Processing**:
   - Scrape prices.
   - Write to Excel.
   - Calculate fair prices.
   - Fetch weather.
   - Send WhatsApp messages to farmers.
   - Log to Google Sheets.
3. **Farmer Reply**:
   - Farmer replies "YES".
   - Webhook `/webhook` receives message.
   - System looks up buyers and replies with list.
   - Logs activity.
