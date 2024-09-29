# main.py

from spotify_auth import get_access_token
from spotify_data import (
    get_top_artists,
    get_saved_albums,
    get_saved_tracks,
    get_top_tracks,
    get_recently_played,
    get_artist_top_tracks
)
from dawg import Dawg
from pprint import pprint

def build_song_hierarchy(access_token):
    # Fetch data from Spotify API
    print("Fetching data from Spotify API...")
    top_artists = get_top_artists(access_token)
    saved_albums = get_saved_albums(access_token)
    saved_tracks = get_saved_tracks(access_token)
    top_tracks = get_top_tracks(access_token)
    recently_played = get_recently_played(access_token)

    # Initialize the song hierarchy
    song_hierarchy = {}

    # Extract genres from top artists
    genres = {}
    for artist in top_artists:
        for genre in artist['genres']:
            genres[genre] = genres.get(genre, [])
            genres[genre].append(artist['name'])

    # Now, for each genre, collect songs from subsets
    for genre_name in genres.keys():
        subsets = {
            "Top Artists": [],
            "Saved Albums": [],
            "Saved Tracks": [],
            "Top Tracks": [],
            "Recently Played": []
        }

        # Top Artists' songs
        for artist in top_artists:
            if genre_name in artist['genres']:
                # Fetch artist's top tracks
                artist_top_tracks = get_artist_top_tracks(access_token, artist['id'])
                subsets["Top Artists"].extend(artist_top_tracks)

        # Saved Albums' tracks
        for album in saved_albums:
            # Check if album artists match the genre's artists
            if any(artist in genres[genre_name] for artist in album['artists']):
                subsets["Saved Albums"].extend(album['tracks'])

        # Saved Tracks
        for track in saved_tracks:
            if any(artist in genres[genre_name] for artist in track['artists']):
                subsets["Saved Tracks"].append(track['name'])

        # Top Tracks
        for track in top_tracks:
            if any(artist in genres[genre_name] for artist in track['artists']):
                subsets["Top Tracks"].append(track['name'])

        # Recently Played
        for track in recently_played:
            if any(artist in genres[genre_name] for artist in track['artists']):
                subsets["Recently Played"].append(track['name'])

        # Remove duplicates in subsets
        for key in subsets:
            subsets[key] = list(set(subsets[key]))

        # Add to song hierarchy
        song_hierarchy[genre_name] = subsets

    return song_hierarchy

def probabilityDistro():
    # Get access token
    access_token, refresh_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token.")
        return None

    # Build the song hierarchy from Spotify data
    song_hierarchy = build_song_hierarchy(access_token)

    # Initialize the DAWG
    dawg = Dawg()

    # Load the DAWG with the song hierarchy
    dawg.load_from_spotify_data(song_hierarchy)

    # Get the genre song counts
    genre_song_counts = dawg.getGenreSongCounts()

    # Return the counts
    return genre_song_counts

if __name__ == '__main__':
    # Call probabilityDistro and get the results
    counts = probabilityDistro()
    if counts:
        # Print the counts
        print("\nGenre Song Counts:")
        pprint(counts)
    else:
        print("Could not retrieve the probability distribution.")
