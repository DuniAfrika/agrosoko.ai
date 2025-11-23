import requests
import os
import json

# WhatsApp Cloud API credentials
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "mock_token")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "mock_phone_id")

def send_whatsapp_message(to_phone, message_body):
    """
    Sends a message via WhatsApp Cloud API.
    """
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message_body}
    }
    
    print(f"Sending WhatsApp message to {to_phone}: {message_body}")
    
    if WHATSAPP_TOKEN == "mock_token":
        print("Mock send successful.")
        return {"status": "success", "mock": True}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return None

def format_daily_message(fair_prices, weather_data, farmer_county):
    """
    Formats the daily 4:45 AM message with enhanced weather information.
    """
    rain_prob = weather_data.get("rainfall_probability", 0)
    rainfall_mm = weather_data.get("rainfall_mm", 0)
    
    # Generate weather comment based on detailed data
    if rain_prob > 70 or rainfall_mm > 15:
        rain_comment = f"⚠️ Heavy rain expected ({rain_prob}% chance, {rainfall_mm}mm). Consider harvesting early or postponing transport."
    elif rain_prob > 50 or rainfall_mm > 5:
        rain_comment = f"☔ Rain likely today ({rain_prob}% chance, {rainfall_mm}mm). Plan accordingly – prices may rise."
    elif rain_prob > 30:
        rain_comment = f"🌤️ Possible light rain ({rain_prob}% chance). Good conditions for most activities."
    else:
        rain_comment = f"☀️ Clear weather expected ({rain_prob}% chance of rain). Excellent for harvesting and transport."
    
    msg = f"""Good morning! 🌾 Here are today's fair farm-gate prices:

• Tomatoes: KSh {fair_prices.get('fair_tomato', 'N/A')}/kg
• Sukuma: KSh {fair_prices.get('fair_sukuma', 'N/A')}/kg
• Onions: KSh {fair_prices.get('fair_onion', 'N/A')}/kg
• Cabbage: KSh {fair_prices.get('fair_cabbage', 'N/A')}/kg

📍 Weather for {farmer_county}:
{rain_comment}

Reply YES if you have produce to sell today."""
    return msg

def format_buyer_list(buyers):
    """
    Formats the buyer list message.
    """
    if not buyers:
        return "No buyers available for your crop today."
        
    msg = "Thanks. Available buyers today:\n\n"
    for i, buyer in enumerate(buyers, 1):
        msg += f"{i}. {buyer['name']} – {buyer['crop']} – KSh {buyer['price']}/kg – {buyer['phone']}\n"
    
    msg += "\nContact them to arrange pickup."
    return msg
