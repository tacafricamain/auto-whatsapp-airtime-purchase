# WhatsApp Flows Backend (Django)

A robust Django backend for handling WhatsApp Flows version 6.0, specifically designed for an airtime purchase use case. This project demonstrates how to handle `INIT` and `data_exchange` actions, decrypt incoming requests, and encrypt responses as required by the WhatsApp Flows API.

## 🚀 Features

- **Flow Version 6.0 Support**: Compatible with the latest WhatsApp Flows schema.
- **Encryption/Decryption**: Implements the required RSA/AES-GCM encryption for secure communication.
- **Data Exchange**: Handles form data submission and returns dynamic responses (e.g., confirmation screens).
- **Health Check**: Includes a compliant health check endpoint for WhatsApp verification.
- **Utility Scripts**: Includes scripts for generating keys and registering them with the WhatsApp Cloud API.

## 🛠️ Prerequisites

- Python 3.8+
- Django 5.0+
- A Meta Developer Account & WhatsApp Business App
- [ngrok](https://ngrok.com/) (for local development)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/whatsapp-flows-backend.git
    cd whatsapp-flows-backend
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generate Encryption Keys:**
    Run the helper script to generate your RSA key pair (`private.pem` and `public.pem`).
    ```bash
    python generate_keys.py
    ```
    *   `private.pem`: Used by the backend to decrypt requests. **Keep this secure.**
    *   `public.pem`: Uploaded to WhatsApp to encrypt requests sent to you.

## ⚙️ Configuration

### 1. WhatsApp Flow Setup
1.  Go to the **WhatsApp Flow Builder** in your Meta Dashboard.
2.  Create a flow using the schema provided in `whatsapp.json`.
3.  **Endpoint URL**: Set this to your public URL (e.g., ngrok) + `/api/flow/`.
    *   Example: `https://your-domain.ngrok-free.app/api/flow/`
4.  **Public Key**: Upload the content of `public.pem` to the Endpoint configuration.

### 2. Register Public Key (Optional)
If you are using the Cloud API and need to register the key programmatically:
1.  Set your `WHATSAPP_ACCESS_TOKEN` and `WHATSAPP_PHONE_ID` environment variables.
2.  Run:
    ```bash
    python register_key.py
    ```

## 🏃‍♂️ Running the Server

1.  **Start Django Server:**
    ```bash
    python manage.py runserver 8000
    ```

2.  **Expose via ngrok:**
    ```bash
    ngrok http 8000
    ```

3.  **Update Endpoint:**
    Copy the HTTPS URL from ngrok and update your WhatsApp Flow configuration.

## 🧪 Testing

### Local Testing
You can test the endpoints locally using `test_endpoint.py`. Note that this script sends plain JSON, so it might fail if the backend strictly enforces encryption (check `views.py` logic).

### Sending a Flow
To send the flow to a user (requires the flow to be Published):
1.  Update `send_flow.py` with your Flow ID and Recipient Phone Number.
2.  Run:
    ```bash
    python send_flow.py
    ```

## 🔒 Security Note

- **Never commit your `.pem` files or `db.sqlite3` to version control.**
- Ensure `DEBUG = False` in production.
- Use environment variables for all sensitive credentials (tokens, IDs).

## 📂 Project Structure

- `airtime_backend/`: Main Django project settings.
- `flows/`: Django app handling the flow logic.
    - `views.py`: Contains the encryption, decryption, and flow handling logic.
- `whatsapp.json`: The JSON definition of the WhatsApp Flow.
- `generate_keys.py`: Script to generate RSA keys.
- `register_key.py`: Script to upload the public key to Meta.

## 📄 License

This project is licensed under the MIT License.
