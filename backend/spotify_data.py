# spotify_data.py

import requests

def get_top_artists(access_token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "limit": 50  # Maximum number of items
    }
    response = requests.get(url, headers=headers, params=params)
    artists = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            artist = {
                'name': item['name'],
                'id': item['id'],
                'genres': item.get('genres', [])
            }
            artists.append(artist)
    else:
        print(f"Error fetching top artists: {response.status_code}")
    return artists

def get_saved_albums(access_token):
    url = "https://api.spotify.com/v1/me/albums"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "limit": 50
    }
    albums = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                album = item['album']
                albums.append({
                    'name': album['name'],
                    'id': album['id'],
                    'artists': [artist['name'] for artist in album['artists']],
                    'tracks': get_album_tracks(access_token, album['id'])
                })
            url = data.get('next')  # Get next page
        else:
            print(f"Error fetching saved albums: {response.status_code}")
            break
    return albums

def get_album_tracks(access_token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "limit": 50
    }
    response = requests.get(url, headers=headers, params=params)
    tracks = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            tracks.append(item['name'])
    else:
        print(f"Error fetching tracks for album {album_id}: {response.status_code}")
    return tracks

def get_saved_tracks(access_token):
    url = "https://api.spotify.com/v1/me/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "limit": 50
    }
    tracks = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                track = item['track']
                tracks.append({
                    'name': track['name'],
                    'id': track['id'],
                    'artists': [artist['name'] for artist in track['artists']],
                    'album': track['album']['name']
                })
            url = data.get('next')  # Get next page
        else:
            print(f"Error fetching saved tracks: {response.status_code}")
            break
    return tracks

def get_top_tracks(access_token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "limit": 50
    }
    response = requests.get(url, headers=headers, params=params)
    tracks = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            tracks.append({
                'name': item['name'],
                'id': item['id'],
                'artists': [artist['name'] for artist in item['artists']],
                'album': item['album']['name']
            })
    else:
        print(f"Error fetching top tracks: {response.status_code}")
    return tracks

def get_recently_played(access_token):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "limit": 50
    }
    response = requests.get(url, headers=headers, params=params)
    tracks = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            track = item['track']
            tracks.append({
                'name': track['name'],
                'id': track['id'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name']
            })
    else:
        print(f"Error fetching recently played tracks: {response.status_code}")
    return tracks

def get_artist_top_tracks(access_token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "market": "US"  # Or any market code
    }
    response = requests.get(url, headers=headers, params=params)
    tracks = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get('tracks', []):
            tracks.append(item['name'])
    else:
        print(f"Error fetching top tracks for artist {artist_id}: {response.status_code}")
    return tracks
