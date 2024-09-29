# dawg_module.py

from spotify_auth import get_access_token
from spotify_data import (
    get_top_artists,
    get_saved_albums,
    get_saved_tracks,
    get_top_tracks,
    get_recently_played,
    get_artist_top_tracks,
    get_audio_features
)
from dawg import Dawg
from database import get_song_reactions
import random

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
    all_song_ids = set()

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
                all_song_ids.update([track['id'] for track in artist_top_tracks])

        # Saved Albums' tracks
        for album in saved_albums:
            # Check if album artists match the genre's artists
            if any(artist in genres[genre_name] for artist in album['artists']):
                subsets["Saved Albums"].extend(album['tracks'])
                all_song_ids.update([track['id'] for track in album['tracks']])

        # Saved Tracks
        for track in saved_tracks:
            if any(artist in genres[genre_name] for artist in track['artists']):
                subsets["Saved Tracks"].append(track)
                all_song_ids.add(track['id'])

        # Top Tracks
        for track in top_tracks:
            if any(artist in genres[genre_name] for artist in track['artists']):
                subsets["Top Tracks"].append(track)
                all_song_ids.add(track['id'])

        # Recently Played
        for track in recently_played:
            if any(artist in genres[genre_name] for artist in track['artists']):
                subsets["Recently Played"].append(track)
                all_song_ids.add(track['id'])

        # Remove duplicates in subsets
        for key in subsets:
            subsets[key] = list({track['id']: track for track in subsets[key]}.values())

        # Add to song hierarchy
        song_hierarchy[genre_name] = subsets

    return song_hierarchy, all_song_ids

def calculate_probability_distribution(genre_song_counts):
    """
    Calculates the probability distribution of songs within each genre and sorts them in descending order.

    Parameters:
    - genre_song_counts: dict of genres mapping to dicts of songs and their weighted counts.

    Returns:
    - genre_probabilities: dict of genres mapping to ordered dicts of songs and their probabilities,
                           sorted from highest to lowest probability.
    """
    genre_probabilities = {}
    for genre, songs in genre_song_counts.items():
        total_weight = sum(songs.values())
        if total_weight == 0:
            continue  # Avoid division by zero
        song_probabilities = {}
        for song_id, weight in songs.items():
            probability = weight / total_weight
            song_probabilities[song_id] = probability

        # Sort the songs by probability in descending order
        sorted_songs = dict(sorted(song_probabilities.items(), key=lambda item: item[1], reverse=True))

        genre_probabilities[genre] = sorted_songs
    return genre_probabilities

def probabilityDistro():
    # Get access token
    access_token, refresh_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token.")
        return None

    # Build the song hierarchy and collect song IDs
    song_hierarchy, all_song_ids = build_song_hierarchy(access_token)

    # Fetch song reactions from the database
    song_reactions = get_song_reactions(all_song_ids)

    # Fetch audio features for all songs
    song_features = get_audio_features(access_token, all_song_ids)

    # Initialize the DAWG
    dawg = Dawg()

    # Load the DAWG with the song hierarchy, reactions, and features
    dawg.load_from_spotify_data(song_hierarchy, song_reactions, song_features)

    # Get the genre song counts
    genre_song_counts = dawg.getGenreSongCounts()

    # Calculate the probability distribution
    genre_probabilities = calculate_probability_distribution(genre_song_counts)

    # Return the probabilities
    return genre_probabilities

def select_next_song(genre_probabilities):
    # Flatten all songs into a list with their probabilities
    songs = []
    probabilities = []
    for genre, song_probs in genre_probabilities.items():
        for song_id, prob in song_probs.items():
            songs.append(song_id)
            probabilities.append(prob)
    if not songs:
        return None
    # Normalize probabilities
    total_prob = sum(probabilities)
    probabilities = [p / total_prob for p in probabilities]
    # Choose a song randomly based on probabilities
    next_song_id = random.choices(songs, weights=probabilities, k=1)[0]
    return next_song_id  # Return the song ID
