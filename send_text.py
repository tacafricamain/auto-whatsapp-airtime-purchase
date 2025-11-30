import requests
import json

import os

# Credentials
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "YOUR_PHONE_NUMBER_ID_HERE")
RECIPIENT_PHONE = "YOUR_RECIPIENT_PHONE_HERE"


def send_text():
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": RECIPIENT_PHONE,
        "type": "text",
        "text": {
            "body": "Hello! This is a test message from your Django backend."
        }
    }
    
    print(f"Sending test message to {RECIPIENT_PHONE}...")
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    send_text()
