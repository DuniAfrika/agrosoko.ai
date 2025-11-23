# 🧪 Test Guide - New Buyer Display Format

## Quick Test (5 minutes)

### Step 1: Start the Server
```bash
cd /Users/ratego/Dev/agrosoko.ai
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Test the New API Endpoint
```bash
# In a new terminal
curl "http://localhost:8000/api/buyers/by-commodity?county=Nairobi" | python -m json.tool
```

**Expected Output:**
```json
{
  "success": true,
  "county": "Nairobi",
  "data": {
    "Tomatoes": [
      {
        "Buyer Name": "Sarova Stanley Hotel",
        "Contact Phone": "+254720123001",
        "Location": "Nairobi CBD",
        ...
      },
      {
        "Buyer Name": "Java House Ltd",
        "Contact Phone": "+254733456002",
        "Location": "Westlands",
        ...
      }
    ],
    "Sukuma": [...],
    "Onions": [...],
    "Cabbage": [...]
  }
}
```

### Step 3: Verify the Data
Check that:
- ✅ Returns 4 commodities (Tomatoes, Sukuma, Onions, Cabbage)
- ✅ Each commodity has max 2 buyers
- ✅ All buyers are from Nairobi
- ✅ Each buyer has: Name, Contact Phone, Location

### Step 4: Test the Agent Flow (Orchestrate)

1. **Update Guideline 3** in Orchestrate:
   - Open `ORCHESTRATE_CONFIG.txt`
   - Find Guideline 3 (line 77)
   - Copy the entire section
   - Paste into Orchestrate

2. **Test the conversation**:
   ```
   User: join agrosoko
   Bot: [Welcome message]
   
   User: start Nairobi
   Bot: [Prices + weather]
   
   User: YES
   Bot: [NEW buyer format - organized by commodity!] ✅
   ```

3. **Verify the response looks like**:
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

## What to Check

### ✅ Format Checklist
- [ ] Message is short and scannable
- [ ] Organized by commodity (not buyer type)
- [ ] Shows 2 buyers per commodity
- [ ] Only shows: Name - Phone - Location
- [ ] Uses commodity emojis (🍅🥬🧅🥗)
- [ ] Phone numbers include +254
- [ ] Total of 8 buyers (2 x 4 commodities)
- [ ] All buyers from Nairobi

### ✅ Comparison with Old Format
- [ ] New format is 50-70% shorter
- [ ] Easier to read on mobile
- [ ] Faster to find phone numbers
- [ ] Better organized

---

## API Endpoints

### New Endpoint (Use This)
```bash
curl "http://localhost:8000/api/buyers/by-commodity?county=Nairobi"
```

### Old Endpoint (Still Works)
```bash
curl "http://localhost:8000/api/buyers?county=Nairobi"
```

### Comparison
```bash
# New: Organized by commodity
curl "http://localhost:8000/api/buyers/by-commodity?county=Nairobi"

# Old: All buyers with full details
curl "http://localhost:8000/api/buyers?county=Nairobi"

# You can test both and compare
```

---

## Troubleshooting

### Issue: API returns empty arrays
**Solution**: Make sure buyers.xlsx has data for Nairobi

### Issue: Less than 2 buyers per commodity
**Solution**: Normal - some commodities may have fewer buyers. Check buyers.xlsx

### Issue: API returns error
**Solution**: 
1. Check server is running
2. Check buyers.xlsx file exists in `/data/` folder
3. Check logs for errors

### Issue: Wrong format in Orchestrate
**Solution**: 
1. Verify you copied Guideline 3 from ORCHESTRATE_CONFIG.txt
2. Check API endpoint URL is correct: `/api/buyers/by-commodity`
3. Verify template uses commodity emojis

---

## Manual Testing Script

```bash
#!/bin/bash

echo "🧪 Testing New Buyer Format..."
echo ""

echo "1. Testing API endpoint..."
response=$(curl -s "http://localhost:8000/api/buyers/by-commodity?county=Nairobi")
echo "$response" | python -m json.tool

echo ""
echo "2. Checking commodity count..."
tomatoes=$(echo "$response" | grep -c "Tomatoes")
sukuma=$(echo "$response" | grep -c "Sukuma")
onions=$(echo "$response" | grep -c "Onions")
cabbage=$(echo "$response" | grep -c "Cabbage")

echo "   Tomatoes: $tomatoes"
echo "   Sukuma: $sukuma"
echo "   Onions: $onions"
echo "   Cabbage: $cabbage"

echo ""
echo "3. Checking Nairobi filter..."
nairobi_count=$(echo "$response" | grep -c "Nairobi")
echo "   Nairobi mentions: $nairobi_count"

echo ""
echo "✅ Test complete!"
```

Save as `test_buyer_format.sh` and run:
```bash
chmod +x test_buyer_format.sh
./test_buyer_format.sh
```

---

## Production Checklist

Before deploying to production:

- [ ] Server running and accessible
- [ ] New API endpoint tested
- [ ] Returns correct data structure
- [ ] Orchestrate guideline updated
- [ ] Test conversation flows
- [ ] Verify mobile display
- [ ] Check all emojis display correctly
- [ ] Test with real farmers (if possible)
- [ ] Monitor for errors
- [ ] Document any issues

---

## Success Criteria

Your implementation is successful when:

✅ API returns buyers organized by 4 commodities  
✅ Each commodity has maximum 2 buyers  
✅ Response is short and scannable  
✅ All buyers are from requested county  
✅ Phone numbers are complete (+254...)  
✅ Emojis display correctly  
✅ Message fits on mobile screen  
✅ Farmers can quickly find contacts  

---

## Next Steps After Testing

1. **If tests pass**:
   - Deploy to production
   - Update Orchestrate
   - Monitor user feedback
   - Track engagement metrics

2. **If adjustments needed**:
   - Modify `buyers_service.py` (change limit)
   - Update templates in guidelines
   - Re-test
   - Deploy

3. **Future enhancements**:
   - Add more commodities
   - Support other counties
   - Rotate top 2 buyers
   - Add buyer ratings

---

**Quick Links:**
- Implementation Details: [UPDATED_BUYER_DISPLAY.md](UPDATED_BUYER_DISPLAY.md)
- Updated Guidelines: [ORCHESTRATE_CONFIG.txt](ORCHESTRATE_CONFIG.txt)
- Template Guide: [BUYER_RESPONSE_TEMPLATE.md](BUYER_RESPONSE_TEMPLATE.md)
- Quick Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Status**: Ready to Test ✅  
**Time to Test**: ~5 minutes  
**Difficulty**: Easy 🟢

