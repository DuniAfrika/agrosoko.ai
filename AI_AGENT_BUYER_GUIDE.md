# AI Agent Guide: How to Show Buyers to Farmers

## Problem Statement
When a farmer says "I want to sell" or similar phrases, the AI agent must display **actual buyer contacts** with all relevant details, not just a generic summary.

## ❌ WRONG Response (Generic Summary)
```
There are 20 buyers in the system, with various types such as hotels, 
restaurants, supermarkets, and wholesalers. The available counties are 
Kiambu, Kisumu, Nairobi, and Nakuru. The buyers have different payment 
terms, price ranges, and quality requirements.
```

## ✅ CORRECT Response (Actual Buyers)
```
Here are verified buyers who want to purchase your produce:

1. 🏨 Sarova Stanley Hotel
   📍 Location: Nairobi CBD
   📞 Contact: +254720123001
   🌾 Buying: Tomatoes, Onions, Cabbage, Sukuma Wiki
   💰 Payment: Net 30 days
   💵 Price Range: KSh 40-55/kg
   📦 Weekly Volume: 500 kg

2. 🍽️ Java House Ltd
   📍 Location: Westlands, Nairobi
   📞 Contact: +254733456002
   🌾 Buying: Tomatoes, Sukuma Wiki, Cabbage
   💰 Payment: Net 15 days
   💵 Price Range: KSh 40-55/kg
   📦 Weekly Volume: 300 kg

3. 🏪 Naivas Supermarket
   📍 Location: Karen, Nairobi
   📞 Contact: +254722890004
   🌾 Buying: All Crops
   💰 Payment: Net 30 days
   💵 Price Range: KSh 35-50/kg
   📦 Weekly Volume: 2,000 kg

Contact these buyers directly to negotiate your sale!
```

---

## API Endpoints to Use

### Option 1: `/api/buyers/for-farmer` (Recommended for AI Agents)

**Best for**: When farmer says "I want to sell" or similar

**URL**: `GET https://agrosoko.keverd.com/api/buyers/for-farmer`

**Parameters**:
- `county` (optional) - Filter by farmer's county
- `limit` (optional) - Number of buyers to show (default: 5, recommend: 3-5)

**Why use this**:
- Clean, simplified format
- Ready for direct display
- Clear instruction field
- Pre-formatted buyer data

**Example Call**:
```bash
GET https://agrosoko.keverd.com/api/buyers/for-farmer?county=Nairobi&limit=3
```

**Response**:
```json
{
  "success": true,
  "count": 3,
  "buyers": [
    {
      "name": "Sarova Stanley Hotel",
      "type": "Hotel",
      "location": "Nairobi CBD",
      "county": "Nairobi",
      "phone": "+254720123001",
      "crops": "Tomatoes, Onions, Cabbage, Sukuma Wiki",
      "weekly_volume_kg": 500,
      "payment_terms": "Net 30",
      "price_range": "40-55",
      "quality_required": "Grade A"
    }
    // ... more buyers
  ],
  "instruction": "Show these buyers to the farmer with their contact details"
}
```

---

### Option 2: `/api/buyers` (Alternative)

**Best for**: When you need all buyer details or specific filtering

**URL**: `GET https://agrosoko.keverd.com/api/buyers`

**Parameters**:
- `county` (optional) - Filter by county
- `buyer_type` (optional) - Filter by type (Hotel, Restaurant, Mama Mboga, Supermarket, Wholesaler)
- `crop` (optional) - Filter by crop (e.g., "Tomatoes", "Sukuma")

**Why use this**:
- Complete buyer database
- All fields included
- Flexible filtering options

**Example Call**:
```bash
GET https://agrosoko.keverd.com/api/buyers?county=Nairobi
```

**Response**:
```json
{
  "count": 17,
  "buyers": [
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
    // ... more buyers
  ]
}
```

---

## Agent Implementation Guide

### Step 1: Detect Farmer Intent
When farmer messages contain:
- "I want to sell"
- "I have produce"
- "YES" (after price information)
- "Where can I sell"
- "Who is buying"
- "Show me buyers"

→ **Action**: Call buyer API

### Step 2: Call the Right Endpoint

**Scenario A: You know farmer's county**
```
GET /api/buyers/for-farmer?county={farmer_county}&limit=3
```

**Scenario B: You don't know farmer's county**
```
GET /api/buyers/for-farmer?limit=5
```

### Step 3: Display Each Buyer Clearly

For each buyer in the response, show:
1. ✅ **Name** - The buyer's business name
2. ✅ **Type** - Hotel, Restaurant, Supermarket, etc.
3. ✅ **Location** - Specific location and county
4. ✅ **Phone** - Contact number (formatted as +254...)
5. ✅ **Crops** - What they're buying
6. ✅ **Payment Terms** - How quickly they pay
7. ✅ **Price Range** - What they offer per kg
8. ✅ **Volume** - How much they buy weekly

### Step 4: Format for WhatsApp/SMS

**Template for each buyer**:
```
{emoji} {name}
📍 {location}, {county}
📞 {phone}
🌾 Buying: {crops}
💰 Payment: {payment_terms}
💵 Price: KSh {price_range}/kg
📦 Volume: {weekly_volume_kg} kg/week
```

**Example**:
```
🏨 Sarova Stanley Hotel
📍 Nairobi CBD, Nairobi
📞 +254720123001
🌾 Buying: Tomatoes, Onions, Cabbage, Sukuma Wiki
💰 Payment: Net 30 days
💵 Price: KSh 40-55/kg
📦 Volume: 500 kg/week
```

---

## Important Rules for AI Agents

### ✅ DO:
1. **Show actual buyer names and contacts** - This is real data, not a summary
2. **Include phone numbers** - Farmers need to contact buyers directly
3. **Format clearly** - Use emojis and line breaks for readability
4. **Limit to 3-5 buyers** - Don't overwhelm the farmer
5. **Match to farmer's county** when possible
6. **Show diverse buyer types** - Mix hotels, restaurants, supermarkets

### ❌ DON'T:
1. **Don't give generic summaries** - "There are 20 buyers..." is useless
2. **Don't hide contact details** - Show the phone numbers!
3. **Don't show buyer IDs** - Farmers don't care about "BYR001"
4. **Don't show ALL buyers** - Too much information is overwhelming
5. **Don't interpret or summarize** - Show the actual data
6. **Don't say "contact us"** - Give direct buyer contacts

---

## Example Conversation Flow

**Farmer**: "I want to sell"

**AI Agent** (Makes API call):
```
GET https://agrosoko.keverd.com/api/buyers/for-farmer?county=Nairobi&limit=3
```

**AI Agent** (Displays response):
```
Great! Here are 3 verified buyers interested in your produce:

1. 🏨 Sarova Stanley Hotel
   📍 Nairobi CBD, Nairobi
   📞 +254720123001
   🌾 Buying: Tomatoes, Onions, Cabbage, Sukuma Wiki
   💰 Payment: Net 30 days
   💵 Price: KSh 40-55/kg
   📦 Volume: 500 kg/week

2. 🍽️ Java House Ltd
   📍 Westlands, Nairobi
   📞 +254733456002
   🌾 Buying: Tomatoes, Sukuma Wiki, Cabbage
   💰 Payment: Net 15 days
   💵 Price: KSh 40-55/kg
   📦 Volume: 300 kg/week

3. 🏪 Naivas Supermarket
   📍 Karen, Nairobi
   📞 +254722890004
   🌾 Buying: All Crops
   💰 Payment: Net 30 days
   💵 Price: KSh 35-50/kg
   📦 Volume: 2,000 kg/week

Call these buyers directly to negotiate your sale! Good luck! 🎉
```

---

## Troubleshooting

### Issue: AI gives generic summary instead of buyer details

**Problem**: The AI might say "There are 20 buyers..." instead of showing actual contacts

**Solution**: Update AI prompt/guidelines to explicitly state:
- "Display the actual buyer names and phone numbers from the API response"
- "Do not summarize - show the complete buyer information"
- "Include all contact details for each buyer"

### Issue: Phone numbers not showing

**Check**: 
1. API response includes "phone" or "Contact Phone" field
2. AI agent is instructed to display phone numbers
3. Format phone numbers with +254 prefix

### Issue: Too many buyers shown

**Solution**: Always use `limit` parameter (recommend 3-5 buyers)
```
GET /api/buyers/for-farmer?limit=3
```

### Issue: Buyers don't match farmer's location

**Solution**: Always pass `county` parameter when known
```
GET /api/buyers/for-farmer?county=Nairobi
```

---

## Testing Your Implementation

### Test 1: Basic Call
```bash
curl "https://agrosoko.keverd.com/api/buyers/for-farmer?limit=2"
```

**Expected**: 2 buyers with full details

### Test 2: County Filter
```bash
curl "https://agrosoko.keverd.com/api/buyers/for-farmer?county=Nairobi&limit=3"
```

**Expected**: 3 buyers from Nairobi

### Test 3: Full Buyer List
```bash
curl "https://agrosoko.keverd.com/api/buyers?county=Nairobi"
```

**Expected**: All Nairobi buyers with complete information

---

## API Response Fields Explanation

| Field | Description | Show to Farmer? |
|-------|-------------|----------------|
| `name` / `Buyer Name` | Business name | ✅ YES |
| `type` / `Buyer Type` | Hotel, Restaurant, etc. | ✅ YES |
| `location` / `Location` | Specific area | ✅ YES |
| `county` / `County` | County | ✅ YES |
| `phone` / `Contact Phone` | Phone number | ✅ YES - IMPORTANT! |
| `crops` / `Crops Interested` | What they buy | ✅ YES |
| `weekly_volume_kg` | Volume needed | ✅ YES |
| `payment_terms` | Payment timeline | ✅ YES |
| `price_range` | Price they offer | ✅ YES |
| `quality_required` | Grade A/B | ✅ Optional |
| `Buyer ID` | Internal ID | ❌ NO |
| `Status` | Active/Inactive | ❌ NO |
| `Verified` | Verification status | ❌ NO |
| `Registration Date` | When registered | ❌ NO |

---

## Quick Reference

**When farmer wants to sell**:
1. Call: `GET /api/buyers/for-farmer?county={county}&limit=3`
2. Loop through `buyers` array
3. Display each buyer with ALL their details
4. Include phone numbers formatted as +254...
5. Use emojis for visual appeal

**Remember**: Farmers need **actual contacts**, not summaries!

---

**Last Updated**: November 23, 2025  
**Production API**: `https://agrosoko.keverd.com`

