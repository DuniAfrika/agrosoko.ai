# AgroGhala API Documentation

Base URL: `http://localhost:8000`

## Smart Caching

🚀 **Performance Feature:** All scraping endpoints use intelligent caching!

- **First request of the day:** Scrapes fresh data from KAMIS
- **Subsequent requests:** Return cached data (instant response!)
- **Cache duration:** Until midnight (resets daily)
- **Force refresh:** Add `?force_refresh=true` to any endpoint

**Benefits:**
- ⚡ Lightning-fast responses
- 🌐 Reduces load on KAMIS servers
- 💰 Efficient bandwidth usage
- 🔄 Automatic daily refresh

## Available Endpoints

### 1. Get KAMIS Market Data (Scraping)

**Endpoint:** `GET /api/scrape/kamis`

**Description:** Scrapes current wholesale prices from KAMIS for all key crops.

**Smart Caching:** Data is cached once scraped for the day. Subsequent requests return cached data (fast!).

**Parameters:**
- `force_refresh` (optional, boolean) - Set to `true` to bypass cache and perform fresh scrape

**Response:**
```json
{
  "success": true,
  "data": {
    "date": "2025-11-21",
    "tomato": 52,
    "sukuma": 21,
    "onion": 68,
    "cabbage": 22,
    "maize": 58,
    "beans": 89,
    "source": "kamis"
  },
  "cached": false,
  "message": "KAMIS data scraped successfully"
}
```

**Examples:**
```bash
# Get data (uses cache if available)
curl http://localhost:8000/api/scrape/kamis

# Force fresh scrape
curl http://localhost:8000/api/scrape/kamis?force_refresh=true
```

---

### 2. Get Weather Data

**Endpoint:** `GET /api/weather/{county}`

**Description:** Gets weather forecast for any Kenyan county.

**Parameters:**
- `county` (path) - Name of Kenyan county (e.g., Nairobi, Kiambu, Mombasa)

**Response:**
```json
{
  "success": true,
  "county": "Nairobi",
  "data": {
    "rainfall_probability": 13,
    "rainfall_mm": 0,
    "source": "Open-Meteo"
  },
  "message": "Weather data for Nairobi retrieved successfully"
}
```

**Examples:**
```bash
# Get weather for Nairobi
curl http://localhost:8000/api/weather/Nairobi

# Get weather for Kiambu
curl http://localhost:8000/api/weather/Kiambu

# Get weather for Mombasa
curl http://localhost:8000/api/weather/Mombasa
```

---

### 3. Get Wholesale Prices

**Endpoint:** `GET /api/prices`

**Description:** Gets current wholesale prices from KAMIS.

**Smart Caching:** Uses cached data if already scraped today.

**Parameters:**
- `force_refresh` (optional, boolean) - Set to `true` to get fresh prices

**Response:**
```json
{
  "success": true,
  "data": {
    "wholesale_prices": {
      "tomato": 52,
      "sukuma": 21,
      "onion": 68,
      "cabbage": 22,
      "maize": 58,
      "beans": 89
    },
    "date": "2025-11-21",
    "source": "kamis"
  },
  "cached": false,
  "message": "Prices retrieved successfully",
  "note": "Prices are in KSh per kg (Nairobi wholesale)"
}
```

**Examples:**
```bash
# Get prices (uses cache)
curl http://localhost:8000/api/prices

# Get fresh prices
curl http://localhost:8000/api/prices?force_refresh=true
```

---

### 4. Get Fair Farm-Gate Prices

**Endpoint:** `GET /api/prices/fair`

**Description:** Calculates fair farm-gate prices from wholesale prices.

**Smart Caching:** Uses cached wholesale prices if available from today.

**Parameters:**
- `force_refresh` (optional, boolean) - Set to `true` to calculate from fresh data

**Response:**
```json
{
  "success": true,
  "data": {
    "fair_prices": {
      "tomato": 39,
      "sukuma": 16,
      "onion": 51,
      "cabbage": 17
    },
    "wholesale_prices": {
      "tomato": 52,
      "sukuma": 21,
      "onion": 68,
      "cabbage": 22
    },
    "date": "2025-11-21"
  },
  "cached": false,
  "message": "Fair prices calculated successfully",
  "note": "Fair price = Wholesale price × 0.75 (farm-gate margin)"
}
```

**Examples:**
```bash
# Get fair prices (uses cache)
curl http://localhost:8000/api/prices/fair

# Calculate from fresh data
curl http://localhost:8000/api/prices/fair?force_refresh=true
```

---

### 5. Get All Buyers

**Endpoint:** `GET /api/buyers`

**Description:** Get all registered buyers with optional filtering.

**Query Parameters:**
- `buyer_type` (optional) - Filter by type (Hotel, Restaurant, Mama Mboga, Supermarket, Wholesaler)
- `county` (optional) - Filter by county
- `crop` (optional) - Filter by crop interest (e.g., "Tomatoes", "Sukuma Wiki")

**Response:**
```json
{
  "success": true,
  "count": 20,
  "data": [
    {
      "Buyer ID": "BYR001",
      "Buyer Name": "Sarova Stanley Hotel",
      "Buyer Type": "Hotel",
      "County": "Nairobi",
      "Location": "Nairobi CBD",
      "Contact Phone": "+254720123001",
      "Crops Interested": "Tomatoes, Onions, Cabbage, Sukuma Wiki",
      "Weekly Volume (kg)": 500,
      "Quality Required": "Grade A",
      "Payment Terms": "Net 30",
      "Price Range (KSh/kg)": "40-55",
      "Status": "Active",
      "Verified": "Yes",
      "Registration Date": "2025-01-15"
    }
  ],
  "filters": {
    "available_types": ["Hotel", "Mama Mboga", "Restaurant", "Restaurant Chain", "Supermarket", "Wholesaler"],
    "available_counties": ["Kiambu", "Kisumu", "Nairobi", "Nakuru"]
  },
  "message": "Retrieved 20 buyers (all buyers)"
}
```

**Examples:**
```bash
# Get all buyers
curl http://localhost:8000/api/buyers

# Filter by type
curl http://localhost:8000/api/buyers?buyer_type=Hotel

# Filter by county
curl http://localhost:8000/api/buyers?county=Nairobi

# Filter by crop
curl http://localhost:8000/api/buyers?crop=Tomatoes
```

---

### 6. Get Buyer by ID

**Endpoint:** `GET /api/buyers/{buyer_id}`

**Description:** Get details of a specific buyer.

**Path Parameters:**
- `buyer_id` - Buyer ID (e.g., "BYR001")

**Response:**
```json
{
  "success": true,
  "data": {
    "Buyer ID": "BYR001",
    "Buyer Name": "Sarova Stanley Hotel",
    "Buyer Type": "Hotel",
    "County": "Nairobi",
    "Location": "Nairobi CBD",
    "Contact Phone": "+254720123001",
    "Crops Interested": "Tomatoes, Onions, Cabbage, Sukuma Wiki",
    "Weekly Volume (kg)": 500,
    "Quality Required": "Grade A",
    "Payment Terms": "Net 30",
    "Price Range (KSh/kg)": "40-55",
    "Status": "Active",
    "Verified": "Yes",
    "Registration Date": "2025-01-15"
  },
  "message": "Buyer BYR001 retrieved"
}
```

**Example:**
```bash
curl http://localhost:8000/api/buyers/BYR001
```

---

### 7. Get Buyer Statistics

**Endpoint:** `GET /api/buyers/stats`

**Description:** Get statistics about all buyers.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_buyers": 20,
    "active_buyers": 20,
    "total_weekly_volume_kg": 25120,
    "buyers_by_type": {
      "Hotel": 4,
      "Mama Mboga": 3,
      "Restaurant": 3,
      "Restaurant Chain": 1,
      "Supermarket": 5,
      "Wholesaler": 4
    },
    "buyers_by_county": {
      "Kiambu": 1,
      "Kisumu": 1,
      "Nairobi": 17,
      "Nakuru": 1
    }
  },
  "message": "Buyer statistics retrieved"
}
```

**Example:**
```bash
curl http://localhost:8000/api/buyers/stats
```

---

### 8. Get Buyer Types

**Endpoint:** `GET /api/buyers/types`

**Description:** Get list of all buyer types.

**Response:**
```json
{
  "success": true,
  "count": 6,
  "data": [
    "Hotel",
    "Mama Mboga",
    "Restaurant",
    "Restaurant Chain",
    "Supermarket",
    "Wholesaler"
  ],
  "message": "Buyer types retrieved"
}
```

**Example:**
```bash
curl http://localhost:8000/api/buyers/types
```

---

### 9. Get All Counties

**Endpoint:** `GET /api/counties`

**Description:** Returns list of all 47 Kenyan counties with GPS coordinates.

**Response:**
```json
{
  "success": true,
  "count": 47,
  "data": [
    {
      "name": "Nairobi",
      "latitude": -1.2864,
      "longitude": 36.8172
    },
    {
      "name": "Mombasa",
      "latitude": -4.0435,
      "longitude": 39.6682
    }
    // ... 45 more counties
  ],
  "message": "All Kenyan counties retrieved"
}
```

**Example:**
```bash
curl http://localhost:8000/api/counties
```

---

### 6. Trigger Daily Workflow

**Endpoint:** `POST /trigger-daily`

**Description:** Manually triggers the complete daily workflow (scraping, weather, messaging).

**Response:**
```json
{
  "status": "Daily workflow triggered"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/trigger-daily
```

---

### 7. Root / Status Check

**Endpoint:** `GET /`

**Description:** Check API status and see all available endpoints.

**Response:**
```json
{
  "status": "AgroGhala Agentic API is running",
  "endpoints": {
    "scraping": "/api/scrape/kamis",
    "weather": "/api/weather/{county}",
    "prices": "/api/prices",
    "fair_prices": "/api/prices/fair",
    "workflow": "/trigger-daily"
  }
}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

## Quick Examples

### Get all data for a farmer

```bash
# 1. Get weather for their county
curl http://localhost:8000/api/weather/Nakuru

# 2. Get current wholesale prices
curl http://localhost:8000/api/prices

# 3. Get fair farm-gate prices
curl http://localhost:8000/api/prices/fair
```

### Test scraping

```bash
# Scrape KAMIS data
curl http://localhost:8000/api/scrape/kamis
```

### Check multiple counties' weather

```bash
# Nairobi
curl http://localhost:8000/api/weather/Nairobi

# Kiambu
curl http://localhost:8000/api/weather/Kiambu

# Nakuru
curl http://localhost:8000/api/weather/Nakuru
```

---

## Interactive API Documentation

Once the server is running, visit:

**Swagger UI:** `http://localhost:8000/docs`

**ReDoc:** `http://localhost:8000/redoc`

These provide interactive API documentation where you can test endpoints directly in your browser!

---

## Error Responses

All endpoints return a consistent error format:

```json
{
  "success": false,
  "error": "Error message details",
  "message": "Human-readable error description"
}
```

---

## Notes

- All prices are in **KSh per kg**
- Weather data updates in real-time from Open-Meteo API
- KAMIS data: First run downloads 18,000 historical rows, subsequent runs get today's data
- No authentication required for read endpoints
- Data is cached for efficiency

