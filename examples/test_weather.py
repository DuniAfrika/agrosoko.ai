"""
Example script demonstrating the weather API service.
This shows how to fetch real weather data for Kenyan counties.
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services import weather_api


def test_single_county():
    """Test weather for a single county."""
    print("=" * 60)
    print("Testing Single County Weather Fetch")
    print("=" * 60)
    
    county = "Nairobi"
    weather = weather_api.get_weather(county)
    
    print(f"\n📍 County: {county}")
    print(f"☔ Rainfall Probability: {weather['rainfall_probability']}%")
    print(f"🌧️  Expected Rainfall: {weather['rainfall_mm']} mm")
    print(f"📡 Data Source: {weather['source']}")
    
    # Provide farming advice based on weather
    if weather['rainfall_probability'] > 70:
        print("⚠️  High chance of rain - Consider postponing harvest")
    elif weather['rainfall_probability'] > 40:
        print("⚠️  Moderate rain chance - Plan accordingly")
    elif weather['rainfall_mm'] > 10:
        print("☔ Heavy rainfall expected - Take precautions")
    else:
        print("✅ Good weather conditions for farming activities")
    

def test_multiple_counties():
    """Test weather for multiple counties."""
    print("\n" + "=" * 60)
    print("Testing Multiple Counties")
    print("=" * 60)
    
    counties = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
        "Machakos", "Meru", "Nyeri", "Kiambu", "Kakamega"
    ]
    
    results = []
    
    for county in counties:
        weather = weather_api.get_weather(county)
        results.append({
            "county": county,
            "probability": weather['rainfall_probability'],
            "rainfall": weather['rainfall_mm'],
            "source": weather['source']
        })
    
    # Sort by rainfall probability
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    print(f"\n{'County':<15} {'Rain Prob':<12} {'Rainfall (mm)':<15} {'Source':<20}")
    print("-" * 65)
    
    for result in results:
        print(f"{result['county']:<15} {result['probability']}%{' ':<10} "
              f"{result['rainfall']:<15} {result['source']:<20}")


def test_coordinates():
    """Test coordinate retrieval for counties."""
    print("\n" + "=" * 60)
    print("Testing County Coordinates")
    print("=" * 60)
    
    test_counties = ["Nairobi", "Mombasa", "Turkana", "Invalid County"]
    
    print(f"\n{'County':<20} {'Latitude':<12} {'Longitude':<12} {'Status'}")
    print("-" * 60)
    
    for county in test_counties:
        coords = weather_api.get_coordinates(county)
        if coords:
            lat, lon = coords
            print(f"{county:<20} {lat:<12.4f} {lon:<12.4f} ✅ Found")
        else:
            print(f"{county:<20} {'N/A':<12} {'N/A':<12} ❌ Not Found")


def test_weather_advisory():
    """Generate weather-based farming advisories."""
    print("\n" + "=" * 60)
    print("Weather-Based Farming Advisories")
    print("=" * 60)
    
    counties = ["Nairobi", "Mombasa", "Kisumu"]
    
    for county in counties:
        weather = weather_api.get_weather(county)
        
        print(f"\n📍 {county}")
        print(f"   Rain Probability: {weather['rainfall_probability']}%")
        print(f"   Expected Rainfall: {weather['rainfall_mm']} mm")
        
        # Generate advisory
        prob = weather['rainfall_probability']
        rain = weather['rainfall_mm']
        
        advisory = []
        if prob > 80 or rain > 20:
            advisory.append("⚠️  Avoid harvesting - high rain expected")
            advisory.append("🌾 Check drainage in fields")
            advisory.append("🚜 Postpone plowing activities")
        elif prob > 50 or rain > 10:
            advisory.append("☔ Moderate rain likely - plan accordingly")
            advisory.append("🌾 Complete urgent harvesting early")
        elif prob < 20 and rain < 2:
            advisory.append("☀️  Excellent weather for farming")
            advisory.append("🌾 Good day for harvesting")
            advisory.append("🚜 Ideal for field work")
        else:
            advisory.append("✅ Normal farming conditions")
            advisory.append("📋 Proceed with planned activities")
        
        for advice in advisory:
            print(f"   {advice}")


if __name__ == "__main__":
    print("\n🌦️  AgroGhala Weather Service Test Suite 🌦️\n")
    
    # Run all tests
    test_single_county()
    test_multiple_counties()
    test_coordinates()
    test_weather_advisory()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n💡 Tip: Set OPENWEATHER_API_KEY environment variable")
    print("   for enhanced weather reliability and backup data.\n")

