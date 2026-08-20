import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("M2M_CLIENT_ID")
CLIENT_SECRET = os.getenv("M2M_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")

API_URL = "http://localhost:3000/api/chat"


# ----------------------------------------------------
# 1. Obtain M2M access token
# ----------------------------------------------------
print("=" * 60)
print("STEP 1 — Obtaining M2M access token")
print("=" * 60)

token_response = requests.post(
    f"https://{AUTH0_DOMAIN}/oauth/token",
    json={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE
    }
)

print("Token endpoint status:", token_response.status_code)

if not token_response.ok:
    print(token_response.text)
    exit()

token_data = token_response.json()

access_token = token_data["access_token"]
expires_in = token_data.get("expires_in")

print("Access token obtained successfully.")
print("Token lifetime:", expires_in, "seconds")
print("Scope:", token_data.get("scope"))


# ----------------------------------------------------
# 2. Call /api/chat with fresh token
# ----------------------------------------------------
print("\n" + "=" * 60)
print("STEP 2 — Calling /api/chat with fresh token")
print("=" * 60)

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(
    API_URL,
    headers=headers
)

if response.status_code == 200:
    print("API status: 200 OK")
else:
    print("API status:", response.status_code)
print("API response:", response.text)


# ----------------------------------------------------
# 3. Wait for token expiration
# ----------------------------------------------------
print("\n" + "=" * 60)
print("STEP 3 — Waiting for token expiration")
print("=" * 60)

print("Waiting 65 seconds...")
time.sleep(65)


# ----------------------------------------------------
# 4. Replay the SAME expired token
# ----------------------------------------------------
print("\n" + "=" * 60)
print("STEP 4 — Replaying expired token")
print("=" * 60)

expired_response = requests.get(
    API_URL,
    headers=headers
)

if expired_response.status_code == 401:
    print("API status: 401 Unauthorized")
else:
    print("API status:", expired_response.status_code)

print("API response:", expired_response.text)

print("\n" + "=" * 60)
print("Credential rotation test completed.")
print("=" * 60)