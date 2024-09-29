# spotify_auth.py

import requests
import urllib.parse
import base64
import webbrowser
from urllib.parse import urlparse, parse_qs

CLIENT_ID = 'c51e5235da0849e3a6b4e04c0b035f2b'         # Replace with your Spotify app's client ID
CLIENT_SECRET = 'f753b4ff61ac4f398d8ff3b0a8a0c70c' # Replace with your Spotify app's client secret
REDIRECT_URI = 'http://10.196.0.110:3000/redirect'
SCOPES = 'user-top-read user-library-read user-read-recently-played'

def get_access_token():
    # Step 1: Redirect user to Spotify's authorization page
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES
    }
    auth_url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)
    print('Opening browser for Spotify authorization...')
    webbrowser.open(auth_url)

    # Step 2: Set up a local server to receive the redirect with the authorization code
    print('Please enter the full redirect URL after authorization:')
    redirect_response = input()

    # Parse the authorization code from the redirect URL
    parsed_url = urlparse(redirect_response)
    code = parse_qs(parsed_url.query).get('code', [None])[0]
    if not code:
        print('Authorization code not found in the URL.')
        return None

    # Step 3: Exchange authorization code for access token
    token_url = 'https://accounts.spotify.com/api/token'
    auth_str = f'{CLIENT_ID}:{CLIENT_SECRET}'
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        print(f'Error obtaining access token: {response.status_code}')
        return None

    token_info = response.json()
    access_token = token_info['access_token']
    refresh_token = token_info.get('refresh_token')

    return access_token, refresh_token

def refresh_access_token(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    auth_str = f'{CLIENT_ID}:{CLIENT_SECRET}'
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code != 200:
        print(f'Error refreshing access token: {response.status_code}')
        return None

    token_info = response.json()
    access_token = token_info['access_token']

    return access_token
