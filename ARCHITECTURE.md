# WhatsApp Flows - Complete Architecture

## 📋 Project Structure

```
whatsapp/
├── airtime_backend/        # Django project settings
│   ├── settings.py         # ✅ Configured with flows app
│   └── urls.py             # ✅ Routes to /api/
├── flows/                  # Django app for WhatsApp Flows
│   ├── views.py            # ✅ Main endpoint logic
│   └── urls.py             # ✅ /flow/ and /health/ endpoints
├── whatsapp.json           # ✅ Flow JSON definition (version 6.0)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── test_endpoint.py        # Local testing script
├── README.md               # Quick start guide
└── NGROK_SETUP.md          # ngrok configuration guide
```

## 🔄 Flow Sequence

### 1. User Opens Flow
```
WhatsApp → Your Backend (INIT action)
```
**Request:**
```json
{
  "action": "INIT",
  "screen": "AIRTIME_PURCHASE"
}
```

**Response:**
```json
{
  "version": "3.0",
  "screen": "AIRTIME_PURCHASE",
  "data": {
    "networks": [
      {"id": "mtn", "title": "MTN"},
      {"id": "glo", "title": "Glo"},
      ...
    ]
  }
}
```

### 2. User Fills Form and Clicks "Continue"
```
WhatsApp → Your Backend (data_exchange action)
```
**Request:**
```json
{
  "action": "data_exchange",
  "screen": "AIRTIME_PURCHASE",
  "data": {
    "network": "mtn",
    "phone": "08011111111",
    "amount": "100"
  }
}
```

**Response:**
```json
{
  "version": "3.0",
  "screen": "CONFIRM_SCREEN",
  "data": {
    "network": "mtn",
    "phone": "08011111111",
    "amount": "100"
  }
}
```

### 3. User Clicks "Confirm & Pay"
```
WhatsApp → Your Webhook (complete action)
```
This sends the final payload to your configured webhook endpoint (not the flow endpoint).

## 🔧 Backend Endpoint Logic

The `flows/views.py` file handles:

1. **INIT Action**: Returns initial screen with network dropdown options
2. **data_exchange Action**: 
   - Receives form data (network, phone, amount)
   - Can perform validation, business logic, API calls, etc.
   - Returns the next screen (CONFIRM_SCREEN) with the data
3. **Error Handling**: Returns proper error responses

## 🌐 URLs Configuration

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/flow/` | POST | Main WhatsApp Flows endpoint |
| `/api/health/` | GET | Health check |

## 📱 WhatsApp Flow Configuration

In the WhatsApp Flow Builder, you need to:

1. **Upload the Flow JSON** (`whatsapp.json`)
2. **Configure the Endpoint URL**: `https://YOUR-NGROK-URL.ngrok-free.app/api/flow/`
3. **Publish the Flow**
4. **Send it to users** via a message template or interactive message

## 🔐 Security Notes

For production, you should:

1. **Verify WhatsApp Signatures**: Add signature verification in `views.py`
2. **Use Environment Variables**: Store secrets in `.env` file
3. **Enable HTTPS**: Use a proper SSL certificate (ngrok provides this)
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Input Validation**: Validate all incoming data

## 🧪 Testing Checklist

- [x] Django server running on port 8000
- [x] Endpoints tested locally with `test_endpoint.py`
- [ ] ngrok installed and configured
- [ ] ngrok tunnel running
- [ ] WhatsApp Flow endpoint configured with ngrok URL
- [ ] Flow tested end-to-end on WhatsApp

## 📊 Monitoring

### Django Logs
Watch the terminal where Django is running to see:
- Incoming requests
- Data being processed
- Responses being sent

### ngrok Web Interface
Open http://127.0.0.1:4040 to see:
- All HTTP requests
- Request/response bodies
- Timing information

## 🚀 Next Steps

1. **Install ngrok** (see `NGROK_SETUP.md`)
2. **Run ngrok**: `ngrok http 8000`
3. **Copy the HTTPS URL** from ngrok output
4. **Configure WhatsApp Flow** with the URL
5. **Test the flow** on WhatsApp

## 💡 Why the Data Wasn't Showing

The issue you experienced (`${data.amount}` showing literally) happens when:

1. **No backend is configured**: The flow tries to use static data only
2. **Backend doesn't respond correctly**: Missing the `data` object in response
3. **Wrong endpoint URL**: WhatsApp can't reach your backend

With this Django backend + ngrok setup, the backend will:
- Receive the form data
- Process it
- Send it back to the confirmation screen
- The variables will be properly replaced with actual values

## 🎯 Expected Result

After setup, when a user:
1. Selects "MTN" as network
2. Enters "08011111111" as phone
3. Enters "100" as amount
4. Clicks "Continue"

They should see:
```
Please confirm your transaction details below.
Network: MTN
Phone: 08011111111
Amount: ₦100
```

Not:
```
Network: ${data.network}
Phone: ${data.phone}
Amount: ₦${data.amount}
```
