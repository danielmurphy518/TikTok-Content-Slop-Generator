import requests
import urllib
import secrets
import time

# Constants
CLIENT_KEY = "sbawkhjfoy0z6ljg2x"
CLIENT_SECRET = "psmcfIMdLYg0aVhPcElwkNdZ7PRXdWIS"
REDIRECT_URI = "https://danieljmurphy.net/callback"
AUTHORIZE_URL = 'https://www.tiktok.com/v2/auth/authorize/'
TOKEN_URL = 'https://open.tiktokapis.com/v2/oauth/token/'

# Function to generate authorization URL
def generate_auth_url():
    csrf_state = secrets.token_hex(16)

    params = {
        'client_key': CLIENT_KEY,
        'scope': 'user.info.basic',
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'state': csrf_state,
    }

    url = AUTHORIZE_URL + '?' + urllib.parse.urlencode(params)
    
    return url, csrf_state

# Function to get the access token
def get_access_token(authorization_code):
    data = {
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(TOKEN_URL, headers=headers, data=urllib.parse.urlencode(data))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        return None

# Testing
def manual_test():
    print("Generating authorization URL...")
    url, state = generate_auth_url()
    print("URL:", url)
    print("State:", state)
    
    # Prompt user for the redirect URL
    input_ = input("Paste the URL you were redirected to: ")
    
    # Extract authorization code from redirect URL
    code = input_.split("code=")[1].split("&")[0]

    # Decode the code (THAT'S THE EDITING PART)
    decoded_code = urllib.parse.unquote(code)

    print("Code:", code)
    print("Decoded Code:", decoded_code)
    
    # Fetch access token without delay
    print("Fetching access token...")
    token_info = get_access_token(decoded_code)
    print(token_info)

if __name__ == "__main__":
    manual_test()
