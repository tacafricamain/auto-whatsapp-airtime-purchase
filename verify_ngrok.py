import requests
import sys

def verify_ngrok():
    print("Paste your current ngrok URL (e.g., https://abc.ngrok-free.app):")
    base_url = input().strip()
    
    if not base_url:
        print("URL is required.")
        return

    # Remove trailing slash if present
    if base_url.endswith('/'):
        base_url = base_url[:-1]
        
    # Construct health check URL
    health_url = f"{base_url}/api/health/"
    flow_url = f"{base_url}/api/flow/"
    
    print(f"\nTesting {health_url}...")
    
    try:
        response = requests.get(health_url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Health check passed! The tunnel is working.")
            print(f"👉 Use this URL in WhatsApp: {flow_url}")
        else:
            print("\n❌ Health check failed. Check your Django server.")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection failed. The URL is unreachable.")
        print("1. Check if ngrok is running.")
        print("2. Check if you copied the correct URL.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    verify_ngrok()
