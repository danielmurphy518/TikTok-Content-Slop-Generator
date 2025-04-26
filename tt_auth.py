import base64
import hashlib
import os
import urllib.parse
import secrets
import requests
from flask import Flask, redirect, request
app = Flask(__name__)
CLIENT_KEY = 'sbawkhjfoy0z6ljg2x'
REDIRECT_URI = 'https://danieljmurphy.net/callback'
SCOPES = 'user.info.stats'
# Generate PKCE challenge
def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge
# Store verifier temporarily
code_verifier, code_challenge = generate_pkce_pair()
@app.route('/')
def auth_redirect():
    encoded_uri = urllib.parse.quote(REDIRECT_URI, safe='')
    auth_url = (
        f"https://www.tiktok.com/v2/auth/authorize/"
        f"?client_key={CLIENT_KEY}"
        f"&response_type=code"
        f"&scope={SCOPES}"
        f"&redirect_uri={encoded_uri}"
        f"&state=random_state_123"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    return redirect(auth_url)
@app.route('/callback')
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization failed.'
    token_url = 'https://open.tiktokapis.com/v2/oauth/token/'
    data = {
        'client_key': CLIENT_KEY,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return f"Token exchange failed: {response.text}"
    token_data = response.json()
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    # Print to console for debugging
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    # Display in browser
    return (
        f"<h1>Access Token</h1><p>{access_token}</p>"
        f"<h1>Refresh Token</h1><p>{refresh_token}</p>"
    )
if __name__ == '__main__':
    app.run(port=5000, debug=True)