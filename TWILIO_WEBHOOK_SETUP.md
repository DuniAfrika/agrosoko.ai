# Twilio Webhook Configuration

## Overview

The AgroGhala API now supports Twilio debugger webhooks to receive error and warning events for monitoring and troubleshooting.

## Webhook Endpoint

**URL**: `https://unclinical-unweighted-dotty.ngrok-free.app/webhook/twilio`

## What It Does

This endpoint receives Twilio debugger events when:
- ❌ Errors occur in your Twilio account
- ⚠️  Warnings are triggered
- 📊 Issues need attention

All events are:
- Logged to console with detailed information
- Optionally logged to Google Sheets (if configured)
- Acknowledged back to Twilio

## Configuration in Twilio Console

### Step 1: Access Twilio Console

1. Log in to [Twilio Console](https://console.twilio.com/)
2. Go to **Monitor** → **Debugger** → **Webhooks**

### Step 2: Set Webhook URL

In the "Set a webhook" section:

**Webhook URL**:
```
https://unclinical-unweighted-dotty.ngrok-free.app/webhook/twilio
```

### Step 3: Save Configuration

1. Click **"Save"** button
2. Twilio will send test events to verify connectivity

## Expected Payload

Twilio sends the following data (as form-encoded):

| Property | Description |
|----------|-------------|
| `AccountSid` | Unique identifier of the account |
| `Sid` | Unique identifier of this debugger event |
| `ParentAccountSid` | Parent account identifier (if subaccount) |
| `Timestamp` | Time of event occurrence |
| `Level` | Severity: `Error` or `Warning` |
| `PayloadType` | Content type: `application/json` |
| `Payload` | JSON data specific to the event |

## What Happens When Event is Received

The webhook will:

1. **Parse the event data**
2. **Log to console**:
   ```
   ======================================================================
   Twilio Debugger Event Received:
     Level: Error
     Timestamp: 2025-11-21T12:34:56Z
     Account: ACxxxxxxxxxxxxx
     Event ID: NOxxxxxxxxxxxxx
     Payload: { ... event details ... }
   ======================================================================
   ```

3. **Log to Google Sheets** (if configured):
   - Farmer Name: "System"
   - Farmer Reply: "Twilio Error" or "Twilio Warning"
   - Buyer List Sent: "Event: NOxxxxxxxxxxxxx"

4. **Return acknowledgment**:
   ```json
   {
     "status": "received",
     "message": "Twilio debugger event logged successfully",
     "event_id": "NOxxxxxxxxxxxxx",
     "level": "Error"
   }
   ```

## Testing the Webhook

### Test with curl

```bash
curl -X POST https://unclinical-unweighted-dotty.ngrok-free.app/webhook/twilio \
  -d "AccountSid=ACxxxxxxxxxxxxx" \
  -d "Sid=NOxxxxxxxxxxxxx" \
  -d "Timestamp=2025-11-21T12:34:56Z" \
  -d "Level=Error" \
  -d "PayloadType=application/json" \
  -d "Payload={\"error_code\":\"30003\",\"message\":\"Test error\"}"
```

### Expected Response

```json
{
  "status": "received",
  "message": "Twilio debugger event logged successfully",
  "event_id": "NOxxxxxxxxxxxxx",
  "level": "Error"
}
```

## Monitoring Events

### View in Console

When the server is running, you'll see events logged:

```bash
./run.sh

# When Twilio event arrives:
======================================================================
Twilio Debugger Event Received:
  Level: Error
  Timestamp: 2025-11-21T12:34:56Z
  Account: ACxxxxxxxxxxxxx
  Event ID: NOxxxxxxxxxxxxx
  Payload: {
    "error_code": "30003",
    "message": "Unreachable destination",
    ...
  }
======================================================================
```

### View in Google Sheets

If Google Sheets is configured, events appear in the Activity Log:

| Date | Farmer Name | County | Prices Sent | Weather Summary | Farmer Reply | Buyer List Sent | Timestamp |
|------|-------------|--------|-------------|-----------------|--------------|-----------------|-----------|
| 2025-11-21 | System | N/A | N/A | N/A | Twilio Error | Event: NOxxxxx | 12:34:56 |

## Common Twilio Error Codes

When you receive webhook events, you might see these error codes:

| Error Code | Description |
|------------|-------------|
| 30003 | Unreachable destination handset |
| 30004 | Message blocked |
| 30005 | Unknown destination handset |
| 30006 | Landline or unreachable carrier |
| 30007 | Message filtered (spam) |
| 30008 | Unknown error |
| 63016 | Number not eligible for SMS |

## Using with Event Streams

Twilio recommends using **Event Streams** for enhanced logging. To use with Event Streams:

1. Go to **Monitor** → **Event Streams**
2. Create a new **HTTP Sink**
3. Set URL to: `https://unclinical-unweighted-dotty.ngrok-free.app/webhook/twilio`
4. Subscribe to error log events
5. Save configuration

## Multiple Webhook Endpoints

You can configure different webhooks for different purposes:

| Endpoint | Purpose |
|----------|---------|
| `/webhook` | WhatsApp Cloud API messages |
| `/webhook/twilio` | Twilio debugger events |

Both endpoints work simultaneously!

## Security Considerations

### For Production:

1. **Validate Twilio Signature**:
   ```python
   from twilio.request_validator import RequestValidator
   
   validator = RequestValidator(os.getenv('TWILIO_AUTH_TOKEN'))
   signature = request.headers.get('X-Twilio-Signature')
   url = str(request.url)
   
   if not validator.validate(url, form_data, signature):
       raise HTTPException(403, "Invalid signature")
   ```

2. **Use HTTPS** (already using ngrok with HTTPS ✅)

3. **Add Rate Limiting** to prevent abuse

4. **Store Events in Database** for long-term analysis

## Troubleshooting

### Webhook Not Receiving Events

**Check:**
1. Server is running: `./run.sh`
2. ngrok is active and URL matches
3. URL in Twilio console is correct
4. No firewall blocking requests

**Test:**
```bash
# Check if endpoint is accessible
curl https://unclinical-unweighted-dotty.ngrok-free.app/

# Test webhook directly
curl -X POST https://unclinical-unweighted-dotty.ngrok-free.app/webhook/twilio \
  -d "Level=Test"
```

### Events Not Logging

**Check:**
1. Console output for error messages
2. Server logs for webhook reception
3. Google Sheets credentials (if using sheets logging)

### Wrong Endpoint

Make sure you're using:
- ✅ `/webhook/twilio` for Twilio events
- ✅ `/webhook` for WhatsApp messages

Don't mix them up!

## Benefits

Using this webhook gives you:

✅ **Real-time error notifications**
✅ **Centralized logging** (console + sheets)
✅ **Easy troubleshooting** with detailed event data
✅ **Historical tracking** of issues
✅ **Integration with existing monitoring**

## Support

### Documentation
- Twilio Debugger: https://www.twilio.com/docs/usage/monitor-debugger
- Event Streams: https://www.twilio.com/docs/events/event-streams
- Webhook Security: https://www.twilio.com/docs/usage/webhooks/webhooks-security

### AgroGhala Resources
- API Documentation: `API.md`
- Main README: `README.md`
- Interactive API Docs: `https://unclinical-unweighted-dotty.ngrok-free.app/docs`

---

**Ready to monitor!** Set the webhook URL in Twilio console and start receiving error/warning events! 📊

