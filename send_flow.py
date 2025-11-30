import requests
import json

import os

# Credentials
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "YOUR_PHONE_NUMBER_ID_HERE")

# User Data
FLOW_ID = "YOUR_FLOW_ID_HERE"
RECIPIENT_PHONE = "YOUR_RECIPIENT_PHONE_HERE"


def send_flow():
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_PHONE,
        "type": "interactive",
        "interactive": {
            "type": "flow",
            "header": {
                "type": "text",
                "text": "Buy Airtime"
            },
            "body": {
                "text": "Click the button below to start the airtime purchase flow."
            },
            "footer": {
                "text": "Powered by Django & WhatsApp Flows"
            },
            "action": {
                "name": "flow",
                "parameters": {
                    "flow_message_version": "3",
                    "flow_token": "test_flow_token_123",
                    "flow_id": FLOW_ID,
                    "flow_cta": "Start Purchase",
                    "flow_action": "navigate",
                    "flow_action_payload": {
                        "screen": "AIRTIME_PURCHASE"
                    }
                }
            }
        }
    }
    
    print(f"Sending flow {FLOW_ID} to {RECIPIENT_PHONE}...")
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    send_flow()
