from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from datetime import datetime

from app.services import kamis_scraper, write_excel, weather_api, price_engine, sheets_logger, whatsapp_agent, buyers_service

app = FastAPI(
    title="AgroGhala API",
    description="Agricultural market intelligence and farmer notification system for Kenya",
    version="1.0.0",
    contact={
        "name": "AgroGhala",
        "url": "https://github.com/yourusername/agrosoko.ai",
    },
    servers=[
        {"url": "https://unclinical-unweighted-dotty.ngrok-free.app", "description": "Public server (ngrok)"},
        {"url": "http://localhost:8000", "description": "Development server"}
    ]
)

class WebhookMessage(BaseModel):
    object: str
    entry: list

@app.get("/")
def read_root():
    return {
        "status": "AgroGhala Agentic API is running",
        "version": "1.0.0",
        "endpoints": {
            "scraping": "/api/scrape/kamis",
            "weather": "/api/weather/{county}",
            "prices": "/api/prices",
            "fair_prices": "/api/prices/fair",
            "counties": "/api/counties",
            "workflow": "/trigger-daily",
            "openapi": "/openapi.json"
        },
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    """
    Get the OpenAPI specification in JSON format.
    Use this for integrations like watsonx Orchestrate.
    """
    return app.openapi()

# =============================================================================
# DATA API ENDPOINTS
# =============================================================================

@app.get("/api/scrape/kamis")
async def scrape_kamis_endpoint(force_refresh: bool = False):
    """
    Scrape KAMIS market data.
    
    Args:
        force_refresh: If true, bypass cache and perform fresh scrape
        
    Returns:
        - Nairobi wholesale prices for key crops
        - Date of data
        - Source (kamis/cache/fallback)
    
    By default, returns cached data if already scraped today.
    Use ?force_refresh=true to force a fresh scrape.
    """
    try:
        prices = kamis_scraper.scrape_kamis(force_refresh=force_refresh)
        
        is_cached = prices.get('source') == 'cache'
        
        return {
            "success": True,
            "data": prices,
            "cached": is_cached,
            "message": "Using cached data from today" if is_cached else "KAMIS data scraped successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to scrape KAMIS data"
        }

@app.get("/api/weather/{county}")
async def get_weather_endpoint(county: str):
    """
    Get weather forecast for a Kenyan county.
    
    Args:
        county: Name of Kenyan county (e.g., Nairobi, Kiambu)
        
    Returns:
        - Rainfall probability (%)
        - Expected rainfall (mm)
        - Data source
    """
    try:
        weather = weather_api.get_weather(county)
        return {
            "success": True,
            "county": county,
            "data": weather,
            "message": f"Weather data for {county} retrieved successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "county": county,
            "error": str(e),
            "message": f"Failed to get weather for {county}"
        }

@app.get("/api/prices")
async def get_prices_endpoint(force_refresh: bool = False):
    """
    Get current wholesale prices from KAMIS.
    
    Args:
        force_refresh: If true, bypass cache and get fresh prices
    
    Returns:
        - Current wholesale prices for all crops
        - Date of data
        - Whether data is cached
        
    By default, uses cached data if available from today.
    """
    try:
        prices = kamis_scraper.scrape_kamis(force_refresh=force_refresh)
        is_cached = prices.get('source') == 'cache'
        
        return {
            "success": True,
            "data": {
                "wholesale_prices": {
                    "tomato": prices.get("tomato"),
                    "sukuma": prices.get("sukuma"),
                    "onion": prices.get("onion"),
                    "cabbage": prices.get("cabbage"),
                    "maize": prices.get("maize"),
                    "beans": prices.get("beans")
                },
                "date": prices.get("date"),
                "source": prices.get("source")
            },
            "cached": is_cached,
            "message": "Using cached prices" if is_cached else "Prices retrieved successfully",
            "note": "Prices are in KSh per kg (Nairobi wholesale)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve prices"
        }

@app.get("/api/prices/fair")
async def get_fair_prices_endpoint(force_refresh: bool = False):
    """
    Get fair farm-gate prices (calculated from wholesale).
    
    Args:
        force_refresh: If true, bypass cache and calculate from fresh data
    
    Returns:
        - Fair farm-gate prices for farmers
        - Calculation method
        - Date of data
        - Whether data is cached
        
    By default, uses cached wholesale prices if available from today.
    """
    try:
        # Get wholesale prices (uses cache if available)
        wholesale_prices = kamis_scraper.scrape_kamis(force_refresh=force_refresh)
        is_cached = wholesale_prices.get('source') == 'cache'
        
        # Calculate fair prices
        fair_prices = price_engine.calculate_fair_prices(wholesale_prices)
        
        return {
            "success": True,
            "data": {
                "fair_prices": {
                    "tomato": fair_prices.get("fair_tomato"),
                    "sukuma": fair_prices.get("fair_sukuma"),
                    "onion": fair_prices.get("fair_onion"),
                    "cabbage": fair_prices.get("fair_cabbage")
                },
                "wholesale_prices": {
                    "tomato": wholesale_prices.get("tomato"),
                    "sukuma": wholesale_prices.get("sukuma"),
                    "onion": wholesale_prices.get("onion"),
                    "cabbage": wholesale_prices.get("cabbage")
                },
                "date": wholesale_prices.get("date")
            },
            "cached": is_cached,
            "message": "Using cached prices" if is_cached else "Fair prices calculated successfully",
            "note": "Fair price = Wholesale price × 0.75 (farm-gate margin)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to calculate fair prices"
        }

@app.get("/api/counties")
async def get_counties_endpoint():
    """
    Get list of all supported Kenyan counties.
    
    Returns:
        - List of 47 Kenyan counties with coordinates
    """
    from app.services.weather_api import KENYA_COUNTIES
    
    counties = [
        {
            "name": name,
            "latitude": coords[0],
            "longitude": coords[1]
        }
        for name, coords in KENYA_COUNTIES.items()
    ]
    
    return {
        "success": True,
        "count": len(counties),
        "data": counties,
        "message": "All Kenyan counties retrieved"
    }

# ============================================================================
# BUYER ENDPOINTS
# ============================================================================

@app.get("/api/buyers")
async def get_all_buyers_endpoint(
    buyer_type: Optional[str] = None,
    county: Optional[str] = None,
    crop: Optional[str] = None
):
    """
    Get all registered buyers or filter by type, county, or crop.
    
    Query Parameters:
        - buyer_type (optional): Filter by buyer type (Hotel, Restaurant, Mama Mboga, Supermarket, Wholesaler)
        - county (optional): Filter by county
        - crop (optional): Filter by crop interest (e.g., "Tomatoes", "Sukuma Wiki")
    
    Returns:
        - List of buyers matching the filters
        - Total count
        - Available filters
    """
    try:
        # Apply filters if provided
        if buyer_type:
            buyers = buyers_service.get_buyers_by_type(buyer_type)
            filter_msg = f"filtered by type: {buyer_type}"
        elif county:
            buyers = buyers_service.get_buyers_by_county(county)
            filter_msg = f"filtered by county: {county}"
        elif crop:
            buyers = buyers_service.get_buyers_by_crop(crop)
            filter_msg = f"filtered by crop: {crop}"
        else:
            buyers = buyers_service.get_all_buyers()
            filter_msg = "all buyers"
        
        return {
            "success": True,
            "count": len(buyers),
            "data": buyers,
            "filters": {
                "available_types": buyers_service.get_buyer_types(),
                "available_counties": buyers_service.get_buyer_counties()
            },
            "message": f"Retrieved {len(buyers)} buyers ({filter_msg})"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve buyers"
        }

@app.get("/api/buyers/stats")
async def get_buyer_stats_endpoint():
    """
    Get statistics about buyers.
    
    Returns:
        - Total buyers
        - Active buyers
        - Total weekly volume capacity
        - Breakdown by type and county
    """
    try:
        stats = buyers_service.get_buyer_stats()
        
        return {
            "success": True,
            "data": stats,
            "message": "Buyer statistics retrieved"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve buyer statistics"
        }

@app.get("/api/buyers/types")
async def get_buyer_types_endpoint():
    """
    Get list of all buyer types.
    
    Returns:
        - List of unique buyer types
    """
    try:
        types = buyers_service.get_buyer_types()
        
        return {
            "success": True,
            "count": len(types),
            "data": types,
            "message": "Buyer types retrieved"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve buyer types"
        }

@app.get("/api/buyers/by-commodity")
async def get_buyers_by_commodity_endpoint(county: str = "Nairobi"):
    """
    Get buyers organized by commodity (2 per crop).
    
    Query Parameters:
        - county (optional): County to filter by (default: Nairobi)
    
    Returns:
        - Buyers organized by commodity (Tomatoes, Sukuma, Onions, Cabbage)
        - 2 buyers per crop with essential info (name, contact, location)
    """
    try:
        buyers_by_crop = buyers_service.get_buyers_by_commodity(county, limit_per_crop=2)
        
        return {
            "success": True,
            "county": county,
            "data": buyers_by_crop,
            "message": f"Buyers organized by commodity for {county}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve buyers by commodity"
        }

@app.get("/api/buyers/{buyer_id}")
async def get_buyer_by_id_endpoint(buyer_id: str):
    """
    Get details of a specific buyer by ID.
    
    Path Parameters:
        - buyer_id: Buyer ID (e.g., "BYR001")
    
    Returns:
        - Buyer details
    """
    try:
        buyer = buyers_service.get_buyer_by_id(buyer_id)
        
        if buyer:
            return {
                "success": True,
                "data": buyer,
                "message": f"Buyer {buyer_id} retrieved"
            }
        else:
            return {
                "success": False,
                "error": f"Buyer {buyer_id} not found",
                "message": "Buyer not found"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve buyer"
        }

# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@app.get("/webhook")
async def whatsapp_webhook_verify(request: Request):
    """
    Handle WhatsApp webhook verification (GET request).
    """
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == os.getenv("WHATSAPP_VERIFY_TOKEN", "my_verify_token"):
        return int(params.get("hub.challenge"))
    return {"error": "Verification failed"}, 403

@app.post("/webhook")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Handle incoming WhatsApp messages from Meta Cloud API.
    Expects JSON payload from WhatsApp Cloud API.
    """
    try:
        # Get content type to determine how to parse
        content_type = request.headers.get("content-type", "")
        
        # Try to parse as JSON (WhatsApp Cloud API sends JSON)
        if "application/json" in content_type:
            data = await request.json()
            print(f"Received WhatsApp webhook data: {data}")
            
            # Extract message details
            try:
                entry = data['entry'][0]
                changes = entry['changes'][0]
                value = changes['value']
                
                if 'messages' in value:
                    message = value['messages'][0]
                    from_phone = message['from']
                    text_body = message['text']['body'].strip().upper()
                    
                    if text_body == "YES":
                        # Trigger YES-reply workflow in background
                        background_tasks.add_task(handle_yes_reply, from_phone)
                        
            except Exception as e:
                print(f"Error processing WhatsApp message: {e}")
                
            return {"status": "received"}
        
        # If not JSON, try form data (might be Twilio or other service)
        else:
            form_data = await request.form()
            print(f"Received form-encoded webhook data: {dict(form_data)}")
            
            # If this looks like a Twilio debugger event, redirect
            if form_data.get("AccountSid") or form_data.get("Level"):
                print("⚠️  Detected Twilio event sent to wrong endpoint!")
                print(f"   Please use /webhook/twilio for Twilio debugger events")
                return {
                    "status": "received",
                    "warning": "Twilio events should be sent to /webhook/twilio"
                }
            
            return {"status": "received", "message": "Non-JSON webhook received"}
            
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/webhook/twilio")
async def twilio_debugger_webhook(request: Request):
    """
    Handle Twilio debugger events (errors and warnings).
    
    Receives error/warning events from Twilio for monitoring and troubleshooting.
    
    Expected payload:
    - AccountSid: Account identifier
    - Sid: Event identifier
    - ParentAccountSid: Parent account (if subaccount)
    - Timestamp: Event occurrence time
    - Level: Error or Warning
    - PayloadType: application/json
    - Payload: Event-specific data
    """
    try:
        # Get form data (Twilio sends as form-encoded)
        form_data = await request.form()
        
        # Extract Twilio debugger event data
        event_data = {
            "AccountSid": form_data.get("AccountSid"),
            "Sid": form_data.get("Sid"),
            "ParentAccountSid": form_data.get("ParentAccountSid"),
            "Timestamp": form_data.get("Timestamp"),
            "Level": form_data.get("Level"),
            "PayloadType": form_data.get("PayloadType"),
            "Payload": form_data.get("Payload")
        }
        
        print(f"=" * 70)
        print(f"Twilio Debugger Event Received:")
        print(f"  Level: {event_data['Level']}")
        print(f"  Timestamp: {event_data['Timestamp']}")
        print(f"  Account: {event_data['AccountSid']}")
        print(f"  Event ID: {event_data['Sid']}")
        
        # Parse the JSON payload if present
        if event_data['Payload']:
            import json
            try:
                payload_json = json.loads(event_data['Payload'])
                print(f"  Payload: {json.dumps(payload_json, indent=2)}")
            except:
                print(f"  Payload: {event_data['Payload']}")
        
        print(f"=" * 70)
        
        # Log to Google Sheets if configured
        try:
            sheets_logger.log_activity(
                farmer_name="System",
                county="N/A",
                prices_sent="N/A",
                weather_summary="N/A",
                farmer_reply=f"Twilio {event_data['Level']}",
                buyer_list_sent=f"Event: {event_data['Sid']}"
            )
        except Exception as e:
            print(f"Could not log to sheets: {e}")
        
        return {
            "status": "received",
            "message": "Twilio debugger event logged successfully",
            "event_id": event_data['Sid'],
            "level": event_data['Level']
        }
        
    except Exception as e:
        print(f"Error processing Twilio webhook: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def handle_yes_reply(phone_number):
    """
    Logic to handle YES reply:
    1. Identify farmer (mock lookup or from sheets)
    2. Find relevant buyers (mock logic: assume they have all crops or ask - for MVP we send all buyers or random)
    3. Send buyer list
    4. Log it
    """
    print(f"Handling YES reply from {phone_number}")
    
    # In a real app, we'd need to know WHICH crop the farmer has. 
    # The prompt implies we just send available buyers.
    # Let's fetch buyers for all 4 crops or just a mix.
    
    # Mock: Fetch buyers for Tomatoes as default or aggregate
    buyers = sheets_logger.get_buyers("Tomato") 
    # Add more if needed
    
    msg = whatsapp_agent.format_buyer_list(buyers)
    whatsapp_agent.send_whatsapp_message(phone_number, msg)
    
    # Log
    sheets_logger.log_activity(
        farmer_name=f"Farmer {phone_number}", # Placeholder if not found
        county="Unknown",
        prices_sent="N/A", # Not sending prices now
        weather_summary="N/A",
        farmer_reply="YES",
        buyer_list_sent="Yes"
    )

@app.post("/trigger-daily")
async def trigger_daily_workflow(background_tasks: BackgroundTasks):
    """
    Manually trigger the daily 4:30 AM workflow.
    """
    background_tasks.add_task(run_daily_workflow)
    return {"status": "Daily workflow triggered"}

def run_daily_workflow():
    print("Starting daily workflow...")
    
    # 1. Scrape KAMIS (force refresh for daily workflow)
    prices = kamis_scraper.scrape_kamis(force_refresh=True)
    
    # 2. Write to Excel
    write_excel.write_to_excel(prices)
    
    # 3. Calculate Fair Prices
    fair_prices = price_engine.calculate_fair_prices(prices)
    
    # 4. Get Farmers
    farmers = sheets_logger.get_farmers()
    
    # 5. Loop through farmers and send messages
    for farmer in farmers:
        county = farmer.get('county', 'Nairobi')
        phone = farmer.get('phone')
        name = farmer.get('name')
        
        # Fetch weather for farmer's county
        weather = weather_api.get_weather(county)
        
        # Format message
        msg = whatsapp_agent.format_daily_message(fair_prices, weather, county)
        
        # Send message
        whatsapp_agent.send_whatsapp_message(phone, msg)
        
        # Log
        sheets_logger.log_activity(
            farmer_name=name,
            county=county,
            prices_sent=str(fair_prices),
            weather_summary=f"Prob: {weather['rainfall_probability']}%",
            farmer_reply="Pending",
            buyer_list_sent="No"
        )
        
    print("Daily workflow completed.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
