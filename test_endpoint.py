import requests
import json

# Test the local endpoint
url = "http://localhost:8000/api/flow/"

# Test 1: INIT action
print("Testing INIT action...")
init_payload = {
    "action": "INIT",
    "screen": "AIRTIME_PURCHASE"
}

response = requests.post(url, json=init_payload)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print("\n" + "="*50 + "\n")

# Test 2: data_exchange action
print("Testing data_exchange action...")
exchange_payload = {
    "action": "data_exchange",
    "screen": "AIRTIME_PURCHASE",
    "data": {
        "network": "mtn",
        "phone": "08011111111",
        "amount": "100"
    }
}

response = requests.post(url, json=exchange_payload)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print("\n" + "="*50 + "\n")

# Test 3: Health check
print("Testing health check...")
health_response = requests.get("http://localhost:8000/api/health/")
print(f"Status: {health_response.status_code}")
print(f"Response: {json.dumps(health_response.json(), indent=2)}")
