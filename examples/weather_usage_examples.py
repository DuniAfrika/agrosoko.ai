"""
Quick Reference: Weather API Usage Examples
============================================
Copy-paste ready code snippets for using the weather service.
"""

# ============================================================================
# BASIC USAGE
# ============================================================================

def example_basic_usage():
    """Simple weather fetch for a single county."""
    from app.services import weather_api
    
    # Get weather for a county
    weather = weather_api.get_weather("Nairobi")
    
    # Access the data
    print(f"Rainfall Probability: {weather['rainfall_probability']}%")
    print(f"Expected Rainfall: {weather['rainfall_mm']} mm")
    print(f"Data Source: {weather['source']}")


# ============================================================================
# INTEGRATION WITH FARMER NOTIFICATIONS
# ============================================================================

def example_farmer_notification():
    """How to use weather data in farmer notifications."""
    from app.services import weather_api
    
    # Farmer's county
    farmer_county = "Kisumu"
    farmer_name = "John Kamau"
    farmer_phone = "+254712345678"
    
    # Get weather
    weather = weather_api.get_weather(farmer_county)
    
    # Build message
    message = f"""
🌾 Good morning {farmer_name}!

📍 Weather for {farmer_county}:
☔ Rain Probability: {weather['rainfall_probability']}%
🌧️ Expected Rainfall: {weather['rainfall_mm']} mm

"""
    
    # Add weather-based advice
    if weather['rainfall_probability'] > 70:
        message += "⚠️ High chance of rain today. Consider postponing harvest.\n"
    elif weather['rainfall_probability'] < 20:
        message += "☀️ Clear weather expected. Good for farming activities!\n"
    
    message += "\n💰 Today's Farm-Gate Prices:\n..."
    
    return message


# ============================================================================
# BATCH PROCESSING FOR MULTIPLE FARMERS
# ============================================================================

def example_batch_processing():
    """Process weather for multiple farmers efficiently."""
    from app.services import weather_api
    
    farmers = [
        {"name": "John Kamau", "county": "Nairobi", "phone": "+254712345678"},
        {"name": "Mary Wanjiku", "county": "Mombasa", "phone": "+254723456789"},
        {"name": "Peter Ochieng", "county": "Kisumu", "phone": "+254734567890"},
    ]
    
    # Cache weather data by county to avoid duplicate API calls
    weather_cache = {}
    
    for farmer in farmers:
        county = farmer['county']
        
        # Check cache first
        if county not in weather_cache:
            weather_cache[county] = weather_api.get_weather(county)
        
        weather = weather_cache[county]
        
        # Now use weather data for this farmer
        print(f"Processing {farmer['name']} ({county})")
        print(f"  Rain: {weather['rainfall_probability']}%")
        # Send notification, log data, etc.


# ============================================================================
# ERROR HANDLING
# ============================================================================

def example_error_handling():
    """Robust weather fetching with error handling."""
    from app.services import weather_api
    
    county = "Nairobi"
    
    try:
        weather = weather_api.get_weather(county)
        
        # Check if using mock data (APIs failed)
        if "Mock" in weather.get('source', ''):
            print("⚠️ Warning: Using mock weather data")
            # Maybe send alert to admin, log error, etc.
        
        # Proceed with weather data
        return weather
        
    except Exception as e:
        print(f"❌ Error fetching weather: {e}")
        # Fallback to default values
        return {
            "rainfall_probability": 50,
            "rainfall_mm": 0,
            "source": "Default (Error)"
        }


# ============================================================================
# CUSTOM WEATHER THRESHOLDS
# ============================================================================

def example_weather_decisions():
    """Make farming decisions based on weather thresholds."""
    from app.services import weather_api
    
    county = "Nakuru"
    weather = weather_api.get_weather(county)
    
    # Define thresholds
    HIGH_RAIN_THRESHOLD = 70  # %
    HEAVY_RAIN_THRESHOLD = 15  # mm
    
    # Make decisions
    decisions = {
        "harvesting_recommended": False,
        "irrigation_needed": False,
        "transport_safe": True,
        "advisory": ""
    }
    
    if weather['rainfall_probability'] > HIGH_RAIN_THRESHOLD:
        decisions['harvesting_recommended'] = False
        decisions['transport_safe'] = False
        decisions['advisory'] = "Postpone harvest due to high rain probability"
        
    elif weather['rainfall_mm'] > HEAVY_RAIN_THRESHOLD:
        decisions['harvesting_recommended'] = False
        decisions['advisory'] = "Heavy rainfall expected - secure crops"
        
    elif weather['rainfall_probability'] < 20:
        decisions['harvesting_recommended'] = True
        decisions['irrigation_needed'] = True
        decisions['advisory'] = "Excellent weather for farming activities"
        
    else:
        decisions['harvesting_recommended'] = True
        decisions['advisory'] = "Normal farming conditions"
    
    return decisions


# ============================================================================
# INTEGRATION WITH LOGGING
# ============================================================================

def example_logging_integration():
    """Log weather data along with other farming activities."""
    from app.services import weather_api
    from datetime import datetime
    
    county = "Nairobi"
    weather = weather_api.get_weather(county)
    
    # Prepare log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "county": county,
        "rainfall_probability": weather['rainfall_probability'],
        "rainfall_mm": weather['rainfall_mm'],
        "weather_source": weather['source'],
        "farmer_notified": True
    }
    
    # Log to Google Sheets, database, or file
    print(f"📝 Logging: {log_entry}")
    
    return log_entry


# ============================================================================
# WEATHER-BASED PRICE ADJUSTMENTS
# ============================================================================

def example_weather_price_adjustment():
    """Adjust prices based on weather conditions."""
    from app.services import weather_api
    
    base_price = 50  # KES per kg
    county = "Meru"
    
    weather = weather_api.get_weather(county)
    
    # Adjust price based on weather
    price_multiplier = 1.0
    
    if weather['rainfall_probability'] > 70:
        # High rain risk - increase price due to transport challenges
        price_multiplier = 1.1
        reason = "Rain expected - transport premium"
        
    elif weather['rainfall_probability'] < 20:
        # Good weather - normal/competitive pricing
        price_multiplier = 1.0
        reason = "Good weather - standard pricing"
        
    else:
        price_multiplier = 1.05
        reason = "Variable weather - slight premium"
    
    adjusted_price = base_price * price_multiplier
    
    return {
        "base_price": base_price,
        "adjusted_price": round(adjusted_price, 2),
        "multiplier": price_multiplier,
        "reason": reason,
        "weather": weather
    }


# ============================================================================
# TESTING AND DEVELOPMENT
# ============================================================================

def example_development_testing():
    """Test weather service during development."""
    from app.services import weather_api
    
    # Test with a list of counties
    test_counties = ["Nairobi", "Mombasa", "InvalidCounty"]
    
    print("Testing Weather Service")
    print("=" * 50)
    
    for county in test_counties:
        try:
            weather = weather_api.get_weather(county)
            status = "✅" if weather else "❌"
            print(f"{status} {county}: {weather['rainfall_probability']}% rain")
        except Exception as e:
            print(f"❌ {county}: Error - {e}")


# ============================================================================
# MAIN DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Weather API Usage Examples")
    print("=" * 70)
    
    print("\n1. Basic Usage:")
    print("-" * 70)
    example_basic_usage()
    
    print("\n2. Farmer Notification:")
    print("-" * 70)
    message = example_farmer_notification()
    print(message)
    
    print("\n3. Batch Processing (with caching):")
    print("-" * 70)
    example_batch_processing()
    
    print("\n4. Error Handling:")
    print("-" * 70)
    weather = example_error_handling()
    print(weather)
    
    print("\n5. Weather-Based Decisions:")
    print("-" * 70)
    decisions = example_weather_decisions()
    print(decisions)
    
    print("\n6. Logging Integration:")
    print("-" * 70)
    log = example_logging_integration()
    print(log)
    
    print("\n7. Weather-Based Price Adjustment:")
    print("-" * 70)
    price_info = example_weather_price_adjustment()
    print(price_info)
    
    print("\n8. Development Testing:")
    print("-" * 70)
    example_development_testing()

