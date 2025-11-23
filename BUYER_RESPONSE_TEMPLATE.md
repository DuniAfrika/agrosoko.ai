# Updated Buyer Response Format

## Overview
When a farmer responds "YES", show buyers organized by commodity with 2 buyers per crop. Focus on Nairobi buyers only.

---

## API Endpoint

**New Endpoint**: `GET /api/buyers/by-commodity?county=Nairobi`

**Response Structure**:
```json
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
    "Sukuma": [
      {
        "Buyer Name": "...",
        "Contact Phone": "+254...",
        "Location": "..."
      }
    ],
    "Onions": [...],
    "Cabbage": [...]
  }
}
```

---

## Response Template (WhatsApp Format)

```
Great! Here are verified buyers in Nairobi:

🍅 TOMATOES
1. [Buyer Name] - [Phone] - [Location]
2. [Buyer Name] - [Phone] - [Location]

🥬 SUKUMA
1. [Buyer Name] - [Phone] - [Location]
2. [Buyer Name] - [Phone] - [Location]

🧅 ONIONS
1. [Buyer Name] - [Phone] - [Location]
2. [Buyer Name] - [Phone] - [Location]

🥗 CABBAGE
1. [Buyer Name] - [Phone] - [Location]
2. [Buyer Name] - [Phone] - [Location]

Contact buyers directly using the phone numbers above.

Start new session: start {county}
```

---

## Example with Real Data

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

---

## Key Changes from Previous Format

### Before (Too Long)
- Showed ALL buyer details (type, weekly volume, payment terms, etc.)
- Listed 10+ buyers
- Very long message
- Hard to read on mobile

### After (Clean & Simple)
- Only essential info: Name, Phone, Location
- Organized by commodity (what they're selling)
- 2 buyers per commodity (8 buyers total)
- Easy to scan and use
- Perfect for WhatsApp

---

## Implementation Steps

### 1. Update Agent Guideline

In **Guideline 3: Buyer List Response**, replace the action with:

```
1. Retrieve user_county from session (default: "Nairobi")
2. Call API: GET /api/buyers/by-commodity?county={user_county}
3. Format response using the template above
4. For each commodity (Tomatoes, Sukuma, Onions, Cabbage):
   - Show emoji + commodity name
   - List 2 buyers with: Name - Phone - Location
5. Add closing message
```

### 2. Update Template in Orchestrate

```
Great! Here are verified buyers in Nairobi:

🍅 TOMATOES
{for each buyer in data.Tomatoes, max 2}
{index}. {Buyer Name} - {Contact Phone} - {Location}
{end for}

🥬 SUKUMA
{for each buyer in data.Sukuma, max 2}
{index}. {Buyer Name} - {Contact Phone} - {Location}
{end for}

🧅 ONIONS
{for each buyer in data.Onions, max 2}
{index}. {Buyer Name} - {Contact Phone} - {Location}
{end for}

🥗 CABBAGE
{for each buyer in data.Cabbage, max 2}
{index}. {Buyer Name} - {Contact Phone} - {Location}
{end for}

Contact buyers directly using the phone numbers above.

Start new session: start {county}
```

---

## Commodity Emojis

| Commodity | Emoji |
|-----------|-------|
| Tomatoes | 🍅 |
| Sukuma | 🥬 |
| Onions | 🧅 |
| Cabbage | 🥗 |

---

## Edge Cases

### No Buyers for a Commodity
If a commodity has 0 buyers:
```
🍅 TOMATOES
No buyers available currently
```

### Only 1 Buyer for a Commodity
Show just 1:
```
🍅 TOMATOES
1. Sarova Stanley Hotel - +254720123001 - Nairobi CBD
```

### API Error
```
⚠️ Unable to load buyer information.

Please try again in a few minutes.
```

---

## Benefits

✅ **Concise**: Short, scannable message  
✅ **Organized**: Grouped by what farmer is selling  
✅ **Actionable**: Phone numbers prominent  
✅ **Mobile-Friendly**: Easy to read on small screens  
✅ **Focused**: Only Nairobi buyers (can expand later)  
✅ **Fast**: 2 buyers per crop = quick decisions  

---

## Testing

Test this format:

```bash
# 1. Start conversation
curl "http://localhost:8000/api/buyers/by-commodity?county=Nairobi"

# 2. Check response structure
# 3. Verify 2 buyers per commodity
# 4. Confirm Nairobi buyers only
```

Expected: Clean, organized JSON with 4 commodities, 2 buyers each.

---

## Version
**Version**: 2.0.0  
**Last Updated**: November 23, 2025  
**Change**: Simplified buyer display format  
**Status**: Production Ready

