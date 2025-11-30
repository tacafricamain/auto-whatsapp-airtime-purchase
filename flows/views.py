import json
import base64
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Load private key
PRIVATE_KEY_PATH = "private.pem"
try:
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        PRIVATE_KEY = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
except FileNotFoundError:
    print("Warning: private.pem not found. Encryption will fail.")
    PRIVATE_KEY = None

def decrypt_request(encrypted_flow_data, encrypted_aes_key, initial_vector):
    try:
        # Decrypt AES key
        aes_key = PRIVATE_KEY.decrypt(
            base64.b64decode(encrypted_aes_key),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt payload
        iv = base64.b64decode(initial_vector)
        encrypted_data = base64.b64decode(encrypted_flow_data)
        tag = encrypted_data[-16:]
        ciphertext = encrypted_data[:-16]
        
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.GCM(iv, tag),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        return json.loads(decrypted_data.decode('utf-8')), aes_key, iv
    except Exception as e:
        print(f"Decryption error: {e}")
        raise

def encrypt_response(response_data, aes_key, iv):
    # Flip IV bits
    flipped_iv = bytearray(iv)
    for i in range(len(flipped_iv)):
        flipped_iv[i] ^= 0xFF
    flipped_iv = bytes(flipped_iv)
    
    # Encrypt response
    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(flipped_iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(json.dumps(response_data).encode('utf-8')) + encryptor.finalize()
    
    return base64.b64encode(ciphertext + encryptor.tag).decode('utf-8')

@csrf_exempt
@require_http_methods(["POST"])
def flow_endpoint(request):
    try:
        body = json.loads(request.body)
        
        # Check if request is encrypted
        if 'encrypted_flow_data' in body:
            decrypted_data, aes_key, iv = decrypt_request(
                body['encrypted_flow_data'],
                body['encrypted_aes_key'],
                body['initial_vector']
            )
            is_encrypted = True
            request_data = decrypted_data
        else:
            is_encrypted = False
            request_data = body

        action = request_data.get('action')
        screen = request_data.get('screen')
        data = request_data.get('data', {})
        
        print(f"Processing action: {action} from screen: {screen}")
        print(f"Received Data: {json.dumps(data, indent=2)}")
        
        response_data = {}
        
        if action == "INIT":
            response_data = {
                "version": "3.0",
                "screen": "AIRTIME_PURCHASE",
                "data": {
                    "networks": [
                        {"id": "mtn", "title": "MTN"},
                        {"id": "glo", "title": "Glo"},
                        {"id": "airtel", "title": "Airtel"},
                        {"id": "9mobile", "title": "9mobile"}
                    ]
                }
            }
        elif action == "data_exchange":
            # Ensure we are coming from the right place, or just process it if it has the right data
            print("Entering data_exchange handler")
            
            # Convert to strings to ensure compatibility with Flow JSON schema
            network_val = str(data.get('network', ''))
            phone_val = str(data.get('phone', ''))
            amount_val = str(data.get('amount', ''))
            
            print(f"Extracted values - Network: {network_val}, Phone: {phone_val}, Amount: {amount_val}")
            
            response_data = {
                "version": "3.0",
                "screen": "CONFIRM_SCREEN",
                "data": {
                    "network": network_val,
                    "phone": phone_val,
                    "amount": amount_val
                }
            }
        elif action == "ping":
            response_data = {
                "data": {
                    "status": "active"
                }
            }
            
        # Return encrypted or plain response
        if is_encrypted:
            encrypted_response = encrypt_response(response_data, aes_key, iv)
            return HttpResponse(encrypted_response, content_type="text/plain")
        else:
            return JsonResponse(response_data)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({"status": "ok"})
