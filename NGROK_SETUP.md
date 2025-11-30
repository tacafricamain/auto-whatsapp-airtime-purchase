# 🚀 Next Steps: Expose Your Backend with ngrok

## What is ngrok?
ngrok creates a secure tunnel from a public URL to your local server, allowing WhatsApp to communicate with your Django backend.

## Installation

### Option 1: Download from Website
1. Go to https://ngrok.com/download
2. Download the Windows version
3. Extract the ZIP file
4. Move `ngrok.exe` to a folder in your PATH (or run it from the download folder)

### Option 2: Using Chocolatey (if installed)
```powershell
choco install ngrok
```

### Option 3: Using Scoop (if installed)
```powershell
scoop install ngrok
```

## Setup

1. **Sign up for a free ngrok account** at https://dashboard.ngrok.com/signup
2. **Get your auth token** from https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure ngrok** with your token:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN
   ```

## Running ngrok

Open a **NEW terminal window** (keep the Django server running in the first one) and run:

```bash
ngrok http 8000
```

You should see output like:
```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123def456.ngrok-free.app -> http://localhost:8000
```

## Configure WhatsApp Flow

1. **Copy the HTTPS forwarding URL** (e.g., `https://abc123def456.ngrok-free.app`)
2. Go to your **WhatsApp Flow** in the Meta Business Suite
3. Click on **Settings** or **Endpoint Configuration**
4. Set the **Endpoint URL** to: `https://abc123def456.ngrok-free.app/api/flow/`
5. **Save** the flow

## Testing

1. Open WhatsApp on your phone
2. Send a message to trigger the flow
3. Fill in the form (network, phone, amount)
4. Click "Continue"
5. You should now see the **confirmation screen** with your actual data (not `${data.amount}`)

## Monitoring Requests

- Open http://127.0.0.1:4040 in your browser to see all incoming requests to your ngrok tunnel
- Check your Django terminal to see the logs

## Troubleshooting

### ngrok session expired
Free ngrok URLs expire after 2 hours. Just restart ngrok and update the URL in WhatsApp Flow.

### "ERR_NGROK_6024"
Your ngrok session limit was reached. Wait a few minutes or upgrade to a paid plan.

### Data not showing on confirmation screen
1. Check the Django logs - you should see the incoming request
2. Check ngrok's web interface (http://127.0.0.1:4040) to see the request/response
3. Ensure the endpoint URL in WhatsApp Flow ends with `/api/flow/`

## Current Status ✅

- ✅ Django server running on http://localhost:8000
- ✅ Endpoints tested and working
- ⏳ Waiting for ngrok setup
- ⏳ Waiting for WhatsApp Flow configuration

## Quick Test Command

Once ngrok is running, test it with:
```bash
curl -X POST https://YOUR-NGROK-URL.ngrok-free.app/api/flow/ \
  -H "Content-Type: application/json" \
  -d '{"action":"INIT","screen":"AIRTIME_PURCHASE"}'
```
