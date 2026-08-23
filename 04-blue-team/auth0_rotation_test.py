import http.server
import threading
import urllib.parse
import webbrowser
import os
import requests


# =========================================================
# AUTH0 CONFIGURATION
# =========================================================

DOMAIN = "dev-7zglzp0amrp0or72.us.auth0.com"
CLIENT_ID = "CrETJm6C4IO6CRwHK1EZxtXqeWtUrfJM"
CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:3000/callback"

# Use the exact Identifier of your Auth0 API.
AUDIENCE = "https://api.securenova.ai"


# =========================================================
# CALLBACK STORAGE
# =========================================================

authorization_code = None
callback_error = None


class CallbackHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        global authorization_code
        global callback_error

        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "error" in params:
            callback_error = params["error"][0]

            if "error_description" in params:
                callback_error += (
                    ": " + params["error_description"][0]
                )

        elif "code" in params:
            authorization_code = params["code"][0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(
            b"""
            <html>
            <body>
            <h2>Auth0 callback received.</h2>
            <p>You can return to the terminal.</p>
            </body>
            </html>
            """
        )

    def log_message(self, format, *args):
        return


# =========================================================
# TOKEN REQUEST
# =========================================================

def request_token(data):

    response = requests.post(
        f"https://{DOMAIN}/oauth/token",
        data=data,
        timeout=30,
    )

    try:
        body = response.json()
    except ValueError:
        body = {"raw_response": response.text}

    return response.status_code, body


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 70)
    print("PROJECT 4 — AUTH0 REFRESH TOKEN ROTATION TEST")
    print("=" * 70)

    if not CLIENT_SECRET:
        print("\n[ERROR] AUTH0_CLIENT_SECRET is not set.")
        return

    # -----------------------------------------------------
    # STEP 1 — CALLBACK SERVER
    # -----------------------------------------------------

    print("\n[STEP 1] STARTING AUTH0 LOGIN")
    print("Starting local callback listener on port 3000...")

    server = http.server.HTTPServer(
        ("localhost", 3000),
        CallbackHandler,
    )

    thread = threading.Thread(
        target=server.handle_request
    )

    thread.daemon = True
    thread.start()

    # -----------------------------------------------------
    # STEP 2 — AUTH0 AUTHORIZATION
    # -----------------------------------------------------

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email offline_access",
        "audience": AUDIENCE,
    }

    authorize_url = (
        f"https://{DOMAIN}/authorize?"
        + urllib.parse.urlencode(params)
    )

    print("Opening Auth0 login page...")

    webbrowser.open(authorize_url)

    thread.join()
    server.server_close()

    if callback_error:
        print("\n[AUTH0 LOGIN ERROR]")
        print(callback_error)
        return

    if not authorization_code:
        print("\n[ERROR] No authorization code received.")
        return

    print("\n[STEP 2] AUTHORIZATION CODE RECEIVED")
    print("Auth0 returned the authorization code.")

    # -----------------------------------------------------
    # STEP 3 — AUTHORIZATION CODE EXCHANGE
    # -----------------------------------------------------

    print("\n[STEP 3] EXCHANGING AUTHORIZATION CODE")

    token_data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
    }

    status, tokens = request_token(token_data)

    print(f"HTTP status: {status}")

    if status != 200:
        print("[ERROR] Authorization code exchange failed.")
        print(tokens)
        return

    refresh_token_1 = tokens.get("refresh_token")

    if not refresh_token_1:
        print("\n[ERROR] No refresh token was returned.")
        print("Confirm offline_access and API offline access.")
        return

    print("Access token received.")
    print("Refresh Token #1 received.")

    # -----------------------------------------------------
    # STEP 4 — FIRST REFRESH
    # -----------------------------------------------------

    print("\n[STEP 4] ROTATING REFRESH TOKEN #1")

    refresh_data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token_1,
    }

    status, rotated_response = request_token(
        refresh_data
    )

    print(f"HTTP status: {status}")

    if status != 200:
        print("[ERROR] First refresh-token exchange failed.")
        print(rotated_response)
        return

    refresh_token_2 = rotated_response.get(
        "refresh_token"
    )

    print("Refresh Token #1 accepted.")
    print("New access token issued.")

    if refresh_token_2:
        print("Refresh Token #2 issued.")
    else:
        print(
            "No new refresh token returned in the response."
        )

    # -----------------------------------------------------
    # STEP 5 — REUSE OLD TOKEN
    # -----------------------------------------------------

    print("\n[STEP 5] REUSING OLD REFRESH TOKEN #1")

    print(
        "Sending the previously used refresh token "
        "to Auth0 again..."
    )

    reuse_data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token_1,
    }

    status, reuse_response = request_token(
        reuse_data
    )

    print(f"HTTP status: {status}")

    print("\n[AUTH0 RESPONSE]")

    print(reuse_response)

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    if status != 200:

        print("\n[SECURITY RESULT]")
        print("OLD REFRESH TOKEN REJECTED")
        print(
            "Auth0 rejected reuse of the previously "
            "rotated refresh token."
        )

    else:

        print("\n[SECURITY RESULT]")
        print("WARNING: OLD REFRESH TOKEN WAS ACCEPTED")
        print(
            "Review refresh-token rotation configuration."
        )


if __name__ == "__main__":
    main()