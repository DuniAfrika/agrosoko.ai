# AgroGhala Agentic MVP

This project implements the AgroGhala Agentic workflow for daily farm-gate price automation.

## Key Features

✅ **Real-Time Weather Data**: Integrated with Open-Meteo API providing accurate weather forecasts for all 47 Kenyan counties
✅ **Automated Price Scraping**: Daily scraping of wholesale prices from KAMIS
✅ **Fair Price Calculation**: Intelligent farm-gate price calculation based on market data
✅ **WhatsApp Integration**: Automated farmer notifications via WhatsApp Cloud API
✅ **Buyer Matching**: Connect farmers with buyers when they respond
✅ **Activity Logging**: Complete audit trail in Google Sheets
✅ **Multi-Tier API Fallback**: Reliable weather data with automatic fallback systems

## Modules

- **kamis_scraper.py**: Intelligent KAMIS data scraper. **First run**: Downloads 3000 historical rows per commodity (18,000 total). **Daily runs**: Fetches only today's data for efficiency. Extracts real Nairobi wholesale prices for Tomatoes, Sukuma, Onions, Cabbage, Maize, and Beans. Saves all data to Excel in `data/` folder.
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

- ✅ KAMIS price scraping (18,000+ rows of real market data)
- ✅ Weather forecasts (all 47 Kenyan counties)
- ✅ Price calculations
- ✅ Excel data exports
- ✅ API endpoints

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

2. **Expose to Internet** (for WhatsApp webhook):
   ```bash
   ngrok http 8000
   ```

3. **Configure WhatsApp Webhook**:
   - URL: `https://<your-domain>/webhook`
   - Verify Token: Match with `WHATSAPP_VERIFY_TOKEN`

4. **Configure watsonx Orchestrate** (optional):
   - Import `workflow.json`
   - Update the URL to your deployed API endpoint

## API Endpoints

Once running, access these endpoints:

- **Scrape KAMIS**: `GET /api/scrape/kamis` - Get latest market prices
- **Weather Data**: `GET /api/weather/{county}` - Get weather for any county
- **Wholesale Prices**: `GET /api/prices` - Get current wholesale prices
- **Fair Prices**: `GET /api/prices/fair` - Get calculated farm-gate prices
- **Counties List**: `GET /api/counties` - Get all 47 Kenyan counties

**Full API Documentation**: See [API.md](API.md)

**Interactive Docs**: Visit `http://localhost:8000/docs` when server is running

**OpenAPI Spec**: Available at `http://localhost:8000/openapi.json` or see `openapi.json` file

**watsonx Orchestrate**: See [WATSONX_INTEGRATION.md](WATSONX_INTEGRATION.md) for integration guide

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
