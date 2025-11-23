# AgroGhala Agent - Quick Reference Card

## 📋 Conversation Flow Summary

```
┌─────────────────────────────────────────────────────────────┐
│  USER: join agrosoko                                        │
│  BOT:  Welcome message + instructions                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  USER: start Nairobi                                        │
│  BOT:  Farm prices + Rain forecast + "Do you have produce?"│
│        (Calls /api/prices/fair + /api/weather/Nairobi)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  USER: YES                                                  │
│  BOT:  List of verified buyers with contact info           │
│        (Calls /api/buyers?county=Nairobi)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Session complete - user can start new session              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Input Patterns

| User Input | Expected Format | Example |
|------------|----------------|---------|
| Join | `join <word>` | `join agrosoko` |
| Start | `start {county}` | `start Nairobi` |
| Confirm | `YES` | `YES` |

---

## ✅ Valid Responses

### Pattern: `join <anything>`
- ✅ `join agrosoko`
- ✅ `JOIN test`
- ✅ `Join hello`
- ❌ `joining` (missing word after join)

### Pattern: `start {county}`
- ✅ `start Nairobi`
- ✅ `START nairobi`
- ✅ `start KIAMBU`
- ❌ `start london` (not a Kenyan county)
- ❌ `started Nairobi` (wrong verb)

### Pattern: `YES` (after receiving prices)
- ✅ `YES`
- ✅ `yes`
- ✅ `Yes`
- ❌ `yes please` (extra words)
- ❌ `yeah` (different word)
- ❌ `ok` (different word)
- ❌ `sure` (different word)

---

## 🔌 API Endpoints Reference

### 1. Get Fair Prices
```
GET /api/prices/fair

Response:
{
  "success": true,
  "data": {
    "fair_prices": {
      "tomato": 117,
      "sukuma": 35,
      "onion": 80,
      "cabbage": 26
    }
  }
}
```

### 2. Get Weather
```
GET /api/weather/{county}

Example: GET /api/weather/Nairobi

Response:
{
  "success": true,
  "data": {
    "rainfall_probability": 18,
    "rainfall_mm": 0
  }
}
```

### 3. Get Buyers (RECOMMENDED - Organized by Commodity)
```
GET /api/buyers/by-commodity?county={county}

Example: GET /api/buyers/by-commodity?county=Nairobi

Response:
{
  "success": true,
  "county": "Nairobi",
  "data": {
    "Tomatoes": [
      {
        "Buyer Name": "Sarova Stanley Hotel",
        "Contact Phone": "+254720123001",
        "Location": "Nairobi CBD"
      },
      {
        "Buyer Name": "Java House Ltd",
        "Contact Phone": "+254733456002",
        "Location": "Westlands"
      }
    ],
    "Sukuma": [...],
    "Onions": [...],
    "Cabbage": [...]
  }
}
```

### 3b. Get All Buyers (Alternative)
```
GET /api/buyers?county={county}

Example: GET /api/buyers?county=Nairobi

Response:
{
  "success": true,
  "count": 17,
  "data": [
    {
      "Buyer Name": "Sarova Stanley Hotel",
      "Buyer Type": "Hotel",
      "County": "Nairobi",
      "Location": "Nairobi CBD",
      "Contact Phone": "+254720123001",
      "Crops Interested": "Tomatoes, Onions, Cabbage, Sukuma Wiki",
      "Weekly Volume (kg)": 500,
      "Payment Terms": "Net 30",
      "Price Range (KSh/kg)": "40-55"
    }
  ]
}
```

---

## 📝 Response Templates

### Template 1: Welcome (after "join")
```
Welcome to AgroGhala! 🌾

You've successfully joined the farm-gate price service for Kenyan farmers.

To get started, send:
start {county}

Example: start Nairobi

Replace {county} with your county name in Kenya.
```

### Template 2: Prices & Weather (after "start")
```
Good morning. Today's fair farm-gate prices:

• Tomatoes: KSh {tomato}/kg
• Sukuma: KSh {sukuma}/kg
• Onions: KSh {onion}/kg
• Cabbage: KSh {cabbage}/kg

Rain update for {county}: {probability}% chance of rain, {mm} mm expected.

Do you have produce to sell today?
```

### Template 3: Buyer List (after "YES") - **NEW SIMPLIFIED FORMAT**
```
Great! Here are verified buyers in Nairobi:

🍅 TOMATOES
1. {Buyer_Name} - {Phone} - {Location}
2. {Buyer_Name} - {Phone} - {Location}

🥬 SUKUMA
1. {Buyer_Name} - {Phone} - {Location}
2. {Buyer_Name} - {Phone} - {Location}

🧅 ONIONS
1. {Buyer_Name} - {Phone} - {Location}
2. {Buyer_Name} - {Phone} - {Location}

🥗 CABBAGE
1. {Buyer_Name} - {Phone} - {Location}
2. {Buyer_Name} - {Phone} - {Location}

Contact buyers directly using the phone numbers above.

Start new session: start {county}
```

**Example:**
```
Great! Here are verified buyers in Nairobi:

🍅 TOMATOES
1. Sarova Stanley Hotel - +254720123001 - Nairobi CBD
2. Java House Ltd - +254733456002 - Westlands

🥬 SUKUMA
1. Mama Njeri's Greengrocers - +254745678003 - Ruaka
2. Carrefour Supermarket - +254722345007 - Junction Mall

🧅 ONIONS
1. Sarova Stanley Hotel - +254720123001 - Nairobi CBD
2. Naivas Supermarket - +254711234567 - Westlands

🥗 CABBAGE
1. Tuskys Supermarket - +254733567890 - CBD
2. Java House Ltd - +254733456002 - Westlands

Contact buyers directly using the phone numbers above.

Start new session: start {county}
```

### Template 4: Invalid County
```
❌ Invalid county name: "{input}"

Please send a valid Kenyan county name.

Format: start {county}

Examples:
- start Nairobi
- start Kiambu
- start Nakuru
- start Mombasa

Need help? Here are some counties: Nairobi, Mombasa, Kisumu, Nakuru, Kiambu, Machakos, Meru, Kilifi
```

### Template 5: Invalid Response
```
❌ Invalid response.

To proceed, please reply with: YES

If you want to start over with a different county, send:
start {county}

Example: start Nairobi
```

### Template 6: Invalid Command
```
❌ Invalid command.

Welcome to AgroGhala! Here's how to use this service:

1️⃣ First time? Join the sandbox:
   join agrosoko

2️⃣ Get farm prices for your county:
   start {county}
   Example: start Nairobi

3️⃣ After receiving prices, respond:
   YES

Need help? Follow the format above to get started.
```

---

## 🌍 Valid Counties (All 47)

```
Baringo, Bomet, Bungoma, Busia, Elgeyo-Marakwet, Embu, Garissa, 
Homa Bay, Isiolo, Kajiado, Kakamega, Kericho, Kiambu, Kilifi, 
Kirinyaga, Kisii, Kisumu, Kitui, Kwale, Laikipia, Lamu, Machakos, 
Makueni, Mandera, Marsabit, Meru, Migori, Mombasa, Murang'a, 
Nairobi, Nakuru, Nandi, Narok, Nyamira, Nyandarua, Nyeri, Samburu, 
Siaya, Taita-Taveta, Tana River, Tharaka-Nithi, Trans Nzoia, 
Turkana, Uasin Gishu, Vihiga, Wajir, West Pokot
```

---

## 🎨 Emoji Guide

### Commodities (Used in Buyer Lists)
| Commodity | Emoji |
|-----------|-------|
| Tomatoes | 🍅 |
| Sukuma | 🥬 |
| Onions | 🧅 |
| Cabbage | 🥗 |

### Buyer Types (Optional - Not Used in New Format)
| Buyer Type | Emoji |
|------------|-------|
| Hotel | 🏨 |
| Restaurant / Restaurant Chain | 🍽️ |
| Mama Mboga | 🛒 |
| Supermarket | 🏪 |
| Wholesaler | 📦 |

### System Messages
| Type | Emoji |
|------|-------|
| Success | ✅ |
| Error | ❌ |
| Warning | ⚠️ |
| Farming | 🌾 |
| Prices | 💰 |
| Rain/Weather | 🌧️ |

---

## ⚙️ Session State Management

| State | Stage | Description | Next Action |
|-------|-------|-------------|-------------|
| 0 | Not Joined | User hasn't sent "join" yet | Prompt to join |
| 1 | Joined | User sent "join", waiting for "start" | Accept "start {county}" |
| 2 | Awaiting Confirmation | Prices sent, waiting for "YES" | Accept only "YES" |
| 3 | Completed | Buyer list sent | Allow new "start {county}" |

---

## 🚨 Error Handling Priority

1. ✅ **API Errors** - Check first, always graceful
2. ✅ **Invalid County** - Validate against 47 counties
3. ✅ **Wrong Response** - "YES" must be exact
4. ✅ **Unknown Command** - Catch-all with help text

---

## 🧪 Test Cases

| Input | Expected Output |
|-------|----------------|
| `join test` | Welcome message |
| `start Nairobi` | Prices + weather for Nairobi |
| `YES` (after prices) | Buyer list for Nairobi |
| `start London` | Invalid county error |
| `maybe` (after prices) | Invalid response error |
| `hello` | Invalid command + help |
| `help` | Support message |

---

## 📞 Support Contact

**Email:** support@agroghala.com  
**Documentation:** See AGENT_GUIDELINE.md for full details  
**Version:** 1.0.0

---

## 🔒 Security Notes

- ✅ Never store farmer personal data beyond phone
- ✅ All buyer info is pre-verified
- ✅ Phone numbers include country code (+254)
- ✅ Session expires after 30 minutes
- ✅ Comply with Kenya Data Protection Act 2019

---

## 💡 Pro Tips

1. **Case Insensitive**: All pattern matching is case-insensitive
2. **Exact Match for YES**: Only "YES" works, not "yes please" or "ok"
3. **County Validation**: Always validate before API call
4. **Session Context**: Store county in session for buyer lookup
5. **Error First**: Always check API success before formatting response
6. **Emoji Consistency**: Use same emoji for same buyer type
7. **Contact Format**: Always `+254XXXXXXXXX` format
8. **Price Format**: Always `KSh X/kg` format

---

## 🎯 Success Metrics

Track these to measure success:
- ✅ Successful "join" commands
- ✅ Valid "start" commands by county
- ✅ "YES" conversions (farmers ready to sell)
- ✅ Buyer contacts provided
- ❌ Error rate by type
- ⏱️ Average response time

---

**Last Updated:** November 23, 2025  
**Status:** Production Ready  
**Maintainer:** AgroGhala Team

