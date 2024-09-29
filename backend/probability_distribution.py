# dawg_module.py

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

def calculate_probability_distribution(genre_song_counts):
    """
    Calculates the probability distribution of songs within each genre.

    Parameters:
    - genre_song_counts: dict of genres mapping to dicts of songs and their weighted counts.

    Returns:
    - genre_probabilities: dict of genres mapping to dicts of songs and their probabilities.
    """
    genre_probabilities = {}
    for genre, songs in genre_song_counts.items():
        total_weight = sum(songs.values())
        if total_weight == 0:
            continue  # Avoid division by zero
        song_probabilities = {}
        for song, weight in songs.items():
            probability = weight / total_weight
            song_probabilities[song] = probability
        genre_probabilities[genre] = song_probabilities
    return genre_probabilities

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

    # Calculate the probability distribution
    genre_probabilities = calculate_probability_distribution(genre_song_counts)

    # Return the probabilities
    return genre_probabilities

if __name__ == '__main__':
    from pprint import pprint

    # Call probabilityDistro and get the results
    genre_probabilities = probabilityDistro()
    if genre_probabilities:
        # Print the probabilities
        print("\nGenre Song Probabilities:")
        for genre, songs in genre_probabilities.items():
            print(f"\nGenre: {genre}")
            for song, probability in songs.items():
                print(f"  {song}: {probability:.2%}")
    else:
        print("Could not retrieve the probability distribution.")