# AgroGhala Agent Guidelines - Implementation Summary

## 📚 Documentation Overview

We've created a comprehensive set of guidelines to ensure consistent, clear, and user-friendly interactions with farmers through the AgroGhala WhatsApp sandbox. This documentation package includes:

### 1. **AGENT_GUIDELINE.md** (Comprehensive)
- **Purpose**: Complete, detailed guide covering all aspects of agent behavior
- **Best For**: Understanding the full system, training new team members, reference documentation
- **Contains**:
  - Full conversation flow with all scenarios
  - Detailed error handling procedures
  - API integration specifications
  - Security and privacy guidelines
  - Logging and monitoring requirements
  - Complete example conversations

### 2. **ORCHESTRATE_GUIDELINE.md** (Platform-Specific)
- **Purpose**: Structured guidelines formatted for IBM watsonx Orchestrate platform
- **Best For**: Direct implementation in Orchestrate, step-by-step setup
- **Contains**:
  - 8 separate guideline definitions
  - Clear conditions and actions for each
  - API endpoint specifications
  - Configuration settings
  - Priority rules

### 3. **QUICK_REFERENCE.md** (At-a-Glance)
- **Purpose**: Quick lookup for templates, patterns, and validation rules
- **Best For**: Day-to-day operations, troubleshooting, quick checks
- **Contains**:
  - Input pattern examples
  - Response templates
  - API endpoint quick reference
  - County list
  - Emoji guide
  - Test cases

### 4. **CONVERSATION_FLOW.md** (Visual)
- **Purpose**: Visual representation of conversation flows and logic
- **Best For**: Understanding flow logic, debugging issues, presenting to stakeholders
- **Contains**:
  - ASCII flow diagrams
  - State transition diagrams
  - Error handling paths
  - API sequence diagrams
  - Complete example conversation

### 5. **ORCHESTRATE_CONFIG.txt** (Copy-Paste Ready)
- **Purpose**: Ready-to-use configuration text for direct copy-paste into Orchestrate
- **Best For**: Quick deployment, reducing setup time, avoiding typos
- **Contains**:
  - 8 guidelines in copy-paste format
  - All templates pre-formatted
  - Configuration values
  - Complete county list
  - Test cases

---

## 🎯 Quick Start - Choose Your Path

### Path A: Using IBM watsonx Orchestrate
1. Open **ORCHESTRATE_CONFIG.txt**
2. Copy each guideline section (1-8) into Orchestrate guideline editor
3. Update API base URL to your production endpoint
4. Test using the test cases provided
5. Refer to **QUICK_REFERENCE.md** for ongoing maintenance

### Path B: Using Other AI Platforms (Dialogflow, Rasa, etc.)
1. Read **AGENT_GUIDELINE.md** for complete understanding
2. Use **CONVERSATION_FLOW.md** to understand logic flow
3. Implement conditions and responses based on your platform's format
4. Use **QUICK_REFERENCE.md** for templates and validation rules
5. Test thoroughly using scenarios in **AGENT_GUIDELINE.md**

### Path C: Custom Implementation
1. Study **AGENT_GUIDELINE.md** for requirements
2. Review **CONVERSATION_FLOW.md** for state management
3. Implement API calls as shown in **ORCHESTRATE_GUIDELINE.md**
4. Use **QUICK_REFERENCE.md** for response templates
5. Test against all scenarios in documentation

---

## 🔄 Conversation Flow Summary

```
User: "join agrosoko"
  ↓
Bot: Welcome message with instructions
  ↓
User: "start Nairobi"
  ↓
Bot: Farm-gate prices + rain forecast + confirmation prompt
  [Calls: /api/prices/fair + /api/weather/Nairobi]
  ↓
User: "YES"
  ↓
Bot: List of verified buyers with contact information
  [Calls: /api/buyers?county=Nairobi]
  ↓
Session complete (user can restart with new county)
```

**Error Handling**: Any invalid input receives specific error message with clear next steps.

---

## 📋 8 Core Guidelines

| # | Guideline | Trigger | Response |
|---|-----------|---------|----------|
| 1 | Sandbox Join | `join <word>` | Welcome message |
| 2 | Price & Weather | `start {county}` (valid) | Prices + weather |
| 3 | Buyer List | `YES` (after prices) | Buyer contacts |
| 4 | Invalid County | `start {invalid}` | County error |
| 5 | Invalid Response | Non-YES after prices | Response error |
| 6 | Invalid Command | Unrecognized input | Help message |
| 7 | API Error | API failure | Service unavailable |
| 8 | Support Request | "help", "support" | Support info |

---

## 🔌 API Endpoints Required

Your agent needs access to these 3 endpoints:

### 1. Get Fair Prices
```
GET /api/prices/fair

Response: {
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

Response: {
  "success": true,
  "data": {
    "rainfall_probability": 18,
    "rainfall_mm": 0
  }
}
```

### 3. Get Buyers
```
GET /api/buyers?county={county}

Response: {
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

## ✅ Validation Rules

### Input Patterns
- **join**: `join <any_word>` (case-insensitive)
- **start**: `start {county}` where county is one of 47 Kenyan counties (case-insensitive)
- **YES**: Exactly "YES" only (case-insensitive), no variations accepted

### County Validation
Must match one of these 47 counties (case-insensitive):
> Baringo, Bomet, Bungoma, Busia, Elgeyo-Marakwet, Embu, Garissa, Homa Bay, Isiolo, Kajiado, Kakamega, Kericho, Kiambu, Kilifi, Kirinyaga, Kisii, Kisumu, Kitui, Kwale, Laikipia, Lamu, Machakos, Makueni, Mandera, Marsabit, Meru, Migori, Mombasa, Murang'a, Nairobi, Nakuru, Nandi, Narok, Nyamira, Nyandarua, Nyeri, Samburu, Siaya, Taita-Taveta, Tana River, Tharaka-Nithi, Trans Nzoia, Turkana, Uasin Gishu, Vihiga, Wajir, West Pokot

### Response Formatting
- **Prices**: Always `KSh X/kg` format
- **Phone Numbers**: Always `+254XXXXXXXXX` format (with country code)
- **Emojis**: Consistent per buyer type (🏨 Hotels, 🍽️ Restaurants, 🛒 Mama Mboga, 🏪 Supermarkets, 📦 Wholesalers)

---

## 🧪 Testing Checklist

Before going live, test these scenarios:

- [ ] ✅ **Valid Join**: `join agrosoko` → Welcome message
- [ ] ✅ **Valid Start**: `start Nairobi` → Prices + weather
- [ ] ✅ **Valid Confirmation**: `YES` → Buyer list
- [ ] ❌ **Invalid County**: `start London` → County error
- [ ] ❌ **Wrong Response**: `maybe` (after prices) → Response error
- [ ] ❌ **Unknown Command**: `hello there` → Help message
- [ ] ℹ️ **Help Request**: `help` → Support message
- [ ] ⚠️ **API Failure**: Simulate API error → Service unavailable message

---

## 🎨 Message Templates

### Welcome (after "join")
```
Welcome to AgroGhala! 🌾

You've successfully joined the farm-gate price service for Kenyan farmers.

To get started, send:
start {county}

Example: start Nairobi

Replace {county} with your county name in Kenya.
```

### Prices & Weather (after "start")
```
Good morning. Today's fair farm-gate prices:

• Tomatoes: KSh 117/kg
• Sukuma: KSh 35/kg
• Onions: KSh 80/kg
• Cabbage: KSh 26/kg

Rain update for Nairobi: 18% chance of rain, 0 mm expected.

Do you have produce to sell today?
```

### Buyer List (after "YES")
```
Great! Here are verified buyers interested in your produce:

🏨 Sarova Stanley Hotel
   Type: Hotel
   Location: Nairobi CBD, Nairobi
   Interested in: Tomatoes, Onions, Cabbage, Sukuma Wiki
   Weekly Volume: 500 kg
   Payment: Net 30
   Price Range: KSh 40-55/kg
   Contact: +254720123001

To connect with a buyer, contact them directly using the phone number provided.

Would you like to start a new session? Send: start {county}
```

---

## 🚨 Common Pitfalls to Avoid

### ❌ Don't Do This
1. Accept "yes please" or "ok" instead of "YES"
2. Accept invalid county names
3. Send buyer info before user confirms "YES"
4. Mix up conversation stages
5. Modify or truncate phone numbers
6. Skip API validation
7. Use inconsistent emojis
8. Assume user's county from previous session

### ✅ Do This Instead
1. Strict "YES" matching (case-insensitive but exact)
2. Validate against 47 county list
3. Always wait for "YES" confirmation
4. Track conversation state properly
5. Send complete, unmodified contact info
6. Check API responses for errors
7. Use emoji guide consistently
8. Always require explicit county input

---

## 📊 Success Metrics

Track these KPIs to measure effectiveness:

| Metric | Target | What It Measures |
|--------|--------|------------------|
| Join Rate | > 90% | Users successfully joining |
| Valid Start Rate | > 85% | Correct county format |
| YES Conversion | > 60% | Farmers ready to sell |
| Error Rate | < 10% | User input errors |
| Response Time | < 3s | System performance |
| Session Completion | > 70% | Full flow completion |

---

## 🔐 Security & Privacy

**Critical Requirements:**
- ✅ Never store farmer personal data beyond phone number
- ✅ All buyer information is pre-verified
- ✅ Phone numbers are validated and active
- ✅ Session data expires after 30 minutes
- ✅ Comply with Kenya Data Protection Act 2019
- ✅ No farmer data shared with buyers without consent

---

## 🆘 Support & Troubleshooting

### Issue: User stuck in conversation
**Solution**: Instruct to send `start {county}` to restart

### Issue: No buyers returned for county
**Solution**: Message shows "No buyers currently available..."

### Issue: API timeout
**Solution**: Show "Service temporarily unavailable" message

### Issue: Invalid county spelling
**Solution**: Show county error with examples

### Issue: User sends variations of "yes"
**Solution**: Only accept exact "YES", show error for others

---

## 🔄 Maintenance & Updates

### When to Update Guidelines
- New counties added (unlikely but possible)
- New buyer types introduced
- API endpoints change
- New error scenarios discovered
- User feedback indicates confusion

### How to Update
1. Update **AGENT_GUIDELINE.md** first (source of truth)
2. Propagate changes to other documents
3. Update **ORCHESTRATE_CONFIG.txt** for deployment
4. Test all scenarios
5. Update version number and date

---

## 📞 Contact & Resources

**Documentation Maintainer**: AgroGhala Team  
**Support Email**: support@agroghala.com  
**API Documentation**: See API.md  
**Version**: 1.0.0  
**Last Updated**: November 23, 2025  

---

## 📦 File Structure

```
/agrosoko.ai/
├── AGENT_GUIDELINE.md           # Comprehensive guide (main reference)
├── ORCHESTRATE_GUIDELINE.md     # Platform-specific structured format
├── ORCHESTRATE_CONFIG.txt       # Copy-paste ready configuration
├── QUICK_REFERENCE.md           # Quick lookup card
├── CONVERSATION_FLOW.md         # Visual flow diagrams
├── GUIDELINES_SUMMARY.md        # This file - overview
├── API.md                       # API documentation
├── README.md                    # Project overview
└── app/
    └── main.py                  # FastAPI server with endpoints
```

---

## 🎓 Learning Path

### For Developers
1. Read **GUIDELINES_SUMMARY.md** (this file) ← You are here
2. Study **CONVERSATION_FLOW.md** for logic understanding
3. Review **AGENT_GUIDELINE.md** for complete specs
4. Implement using **ORCHESTRATE_CONFIG.txt**
5. Keep **QUICK_REFERENCE.md** handy for daily work

### For Product Managers
1. Read **GUIDELINES_SUMMARY.md** (this file) ← You are here
2. Review **CONVERSATION_FLOW.md** for user experience
3. Check **AGENT_GUIDELINE.md** for business rules
4. Use **QUICK_REFERENCE.md** for testing/validation

### For Support Team
1. Read **QUICK_REFERENCE.md** for templates
2. Review **CONVERSATION_FLOW.md** for troubleshooting
3. Keep **AGENT_GUIDELINE.md** for edge cases
4. Use test cases for validation

---

## 🚀 Deployment Checklist

Before going live:

- [ ] All 8 guidelines configured in agent platform
- [ ] API base URL updated to production endpoint
- [ ] API endpoints tested and responding correctly
- [ ] All 8 test cases passing
- [ ] Session management working (30-minute timeout)
- [ ] Error handling tested (API failures)
- [ ] County validation working (all 47 counties)
- [ ] Buyer list formatting correct (emojis, phone numbers)
- [ ] Response times under 3 seconds
- [ ] Logging/monitoring configured
- [ ] Support contact information correct
- [ ] Privacy compliance verified

---

## 🎯 Next Steps

### Immediate (Week 1)
1. ✅ Implement 8 core guidelines
2. ✅ Test all scenarios
3. ✅ Deploy to staging environment
4. ✅ Get internal team feedback

### Short Term (Month 1)
1. 📊 Monitor user interactions
2. 🔧 Fix any discovered issues
3. 📈 Track success metrics
4. 🎨 Refine messaging based on feedback

### Long Term (Quarter 1)
1. 🌍 Expand to more counties (if needed)
2. 🛒 Add more buyers to directory
3. 📱 Enhance user experience
4. 🤖 Improve AI responses based on data

---

## ✨ Key Takeaways

1. **Strict Flow**: Users must follow join → start → YES sequence
2. **Exact Matching**: "YES" must be exact, counties must be valid
3. **Clear Errors**: Every invalid input gets helpful error message
4. **API Integration**: Three endpoints provide all necessary data
5. **Consistent Formatting**: Templates ensure uniform user experience
6. **Error Handling**: Graceful degradation when APIs fail
7. **State Management**: Session tracking enables multi-step conversations
8. **Testing**: Comprehensive test cases ensure reliability

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: November 23, 2025

---

*Thank you for implementing AgroGhala! Together, we're helping Kenyan farmers get fair prices and connecting them with verified buyers. 🌾*

