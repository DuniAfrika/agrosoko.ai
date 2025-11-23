import requests
import os
from datetime import datetime
from typing import Dict, Tuple, Optional

# Kenyan Counties with their approximate coordinates (latitude, longitude)
KENYA_COUNTIES = {
    "Nairobi": (-1.2864, 36.8172),
    "Mombasa": (-4.0435, 39.6682),
    "Kisumu": (-0.0917, 34.7680),
    "Nakuru": (-0.3031, 36.0800),
    "Kiambu": (-1.1714, 36.8356),
    "Machakos": (-1.5177, 37.2634),
    "Meru": (0.0500, 37.6500),
    "Nyeri": (-0.4167, 36.9500),
    "Eldoret": (0.5143, 35.2698),
    "Kakamega": (0.2827, 34.7519),
    "Kajiado": (-2.0979, 36.7819),
    "Kilifi": (-3.5106, 39.9094),
    "Kwale": (-4.1811, 39.4520),
    "Migori": (-1.0634, 34.4731),
    "Turkana": (3.1197, 35.5986),
    "Garissa": (-0.4536, 39.6401),
    "Wajir": (1.7471, 40.0573),
    "Mandera": (3.9366, 41.8669),
    "Lamu": (-2.2717, 40.9020),
    "Tana River": (-1.5240, 39.9946),
    "Taita Taveta": (-3.3167, 38.4833),
    "Embu": (-0.5396, 37.4570),
    "Kitui": (-1.3667, 38.0167),
    "Makueni": (-2.9667, 37.8333),
    "Nyandarua": (-0.1833, 36.5333),
    "Nyamira": (-0.5667, 34.9333),
    "Kisii": (-0.6817, 34.7680),
    "Siaya": (-0.0617, 34.2883),
    "Busia": (0.4350, 34.1117),
    "Bungoma": (0.5635, 34.5606),
    "Trans Nzoia": (1.0500, 35.0000),
    "Uasin Gishu": (0.5500, 35.3000),
    "Elgeyo Marakwet": (0.8333, 35.3333),
    "Nandi": (0.1833, 35.1167),
    "Baringo": (0.6667, 36.0833),
    "Laikipia": (0.3667, 36.7833),
    "Samburu": (1.2167, 36.8000),
    "Marsabit": (2.3333, 37.9833),
    "Isiolo": (0.3556, 37.5828),
    "West Pokot": (1.6167, 35.1167),
    "Vihiga": (0.0667, 34.7167),
    "Kericho": (-0.3667, 35.2833),
    "Bomet": (-0.7833, 35.3000),
    "Narok": (-1.0833, 35.8667),
    "Kirinyaga": (-0.5000, 37.3833),
    "Murang'a": (-0.7167, 37.1500),
    "Tharaka Nithi": (-0.2833, 37.6667),
}


def get_coordinates(county: str) -> Optional[Tuple[float, float]]:
    """
    Get latitude and longitude for a Kenyan county.
    Returns: (latitude, longitude) or None if county not found
    """
    return KENYA_COUNTIES.get(county)


def get_weather_open_meteo(lat: float, lon: float) -> Dict:
    """
    Fetch weather data from Open-Meteo API (free, no API key required).
    Returns weather forecast including precipitation probability and amount.
    """
    try:
        # Open-Meteo API endpoint
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "precipitation_probability,precipitation",
            "daily": "precipitation_sum,precipitation_probability_max",
            "timezone": "Africa/Nairobi",
            "forecast_days": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract daily data
        daily = data.get("daily", {})
        rainfall_mm = daily.get("precipitation_sum", [0])[0] or 0
        rainfall_prob = daily.get("precipitation_probability_max", [0])[0] or 0
        
        # If daily data is missing, use hourly averages
        if rainfall_mm == 0 and rainfall_prob == 0:
            hourly = data.get("hourly", {})
            precip_list = hourly.get("precipitation", [])
            prob_list = hourly.get("precipitation_probability", [])
            
            if precip_list:
                rainfall_mm = sum(precip_list) / len(precip_list)
            if prob_list:
                rainfall_prob = max(prob_list)
        
        return {
            "rainfall_probability": int(rainfall_prob),
            "rainfall_mm": round(rainfall_mm, 1),
            "source": "Open-Meteo"
        }
        
    except Exception as e:
        print(f"Error fetching from Open-Meteo: {e}")
        return None


def get_weather_openweathermap(lat: float, lon: float, api_key: str) -> Dict:
    """
    Fetch weather data from OpenWeatherMap API (requires API key).
    Provides more detailed and reliable weather data.
    """
    try:
        # OpenWeatherMap One Call API 3.0 (or use current weather + forecast)
        url = "https://api.openweathermap.org/data/2.5/forecast"
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Calculate average rainfall and probability from forecast
        forecasts = data.get("list", [])[:8]  # Next 24 hours (3-hour intervals)
        
        total_rain = 0
        rain_count = 0
        max_clouds = 0
        
        for forecast in forecasts:
            rain = forecast.get("rain", {}).get("3h", 0)
            total_rain += rain
            
            if rain > 0:
                rain_count += 1
                
            clouds = forecast.get("clouds", {}).get("all", 0)
            max_clouds = max(max_clouds, clouds)
        
        rainfall_mm = total_rain
        # Estimate probability based on rainy periods and cloud cover
        rainfall_prob = int((rain_count / len(forecasts)) * 100) if forecasts else 0
        rainfall_prob = max(rainfall_prob, int(max_clouds * 0.7))  # Cloud-based estimate
        
        return {
            "rainfall_probability": min(rainfall_prob, 100),
            "rainfall_mm": round(rainfall_mm, 1),
            "source": "OpenWeatherMap"
        }
        
    except Exception as e:
        print(f"Error fetching from OpenWeatherMap: {e}")
        return None


def get_weather(county: str) -> Dict:
    """
    Fetches rainfall probability and amount for a given Kenyan county.
    
    Uses multiple weather APIs with fallback:
    1. Open-Meteo (free, no API key)
    2. OpenWeatherMap (if API key is provided)
    3. Mock data (as last resort)
    
    Args:
        county: Name of the Kenyan county
        
    Returns:
        Dictionary with:
        - rainfall_probability: int (0-100%)
        - rainfall_mm: float (millimeters)
        - source: str (API source used)
    """
    print(f"Fetching weather for {county}...")
    
    # Get coordinates for the county
    coords = get_coordinates(county)
    
    if not coords:
        print(f"Warning: County '{county}' not found in database. Using Nairobi as default.")
        coords = KENYA_COUNTIES["Nairobi"]
    
    lat, lon = coords
    print(f"Coordinates: {lat}, {lon}")
    
    # Try Open-Meteo first (free, no API key required)
    weather_data = get_weather_open_meteo(lat, lon)
    
    # If Open-Meteo fails, try OpenWeatherMap (if API key available)
    if not weather_data:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if api_key:
            print("Trying OpenWeatherMap API...")
            weather_data = get_weather_openweathermap(lat, lon, api_key)
    
    # If all APIs fail, use mock data as fallback
    if not weather_data:
        print("Warning: All weather APIs failed. Using mock data.")
        import random
        weather_data = {
            "rainfall_probability": random.randint(20, 80),
            "rainfall_mm": round(random.uniform(0, 20), 1),
            "source": "Mock (API unavailable)"
        }
    
    print(f"Weather for {county}: {weather_data}")
    return weather_data


if __name__ == "__main__":
    # Test the weather service
    test_counties = ["Nairobi", "Mombasa", "Kisumu", "Nakuru"]
    
    for county in test_counties:
        print(f"\n{'='*50}")
        weather = get_weather(county)
        print(f"County: {county}")
        print(f"Rainfall Probability: {weather['rainfall_probability']}%")
        print(f"Expected Rainfall: {weather['rainfall_mm']} mm")
        print(f"Data Source: {weather['source']}")
        print('='*50)
