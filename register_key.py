import requests

import os

# Credentials
# Replace these with your actual values or set them as environment variables
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "YOUR_PHONE_NUMBER_ID_HERE")


def register_key():
    try:
        # Read the existing public key
        with open("public.pem", "r") as f:
            public_key = f.read()

        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/whatsapp_business_encryption"
        
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        
        data = {
            "business_public_key": public_key
        }
        
        print(f"Registering key for Phone ID: {PHONE_NUMBER_ID}...")
        response = requests.post(url, headers=headers, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except FileNotFoundError:
        print("Error: public.pem not found. Please ensure keys are generated first.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    register_key()
