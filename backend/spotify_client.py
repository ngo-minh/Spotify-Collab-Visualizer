import time
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv
from hashmap import HashMap
from heap import Heap
import threading
from functools import wraps

# rate limit protection
# https://www.w3resource.com/python-exercises/decorator/python-decorator-exercise-7.php
lock = threading.Lock()
thread_local = threading.local()

# decorator to make sure Spotify don't get requests too fast
def rate_limited(max_per_second):
    min_interval = 1.0 / max_per_second

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not hasattr(thread_local, 'last_called'):
                thread_local.last_called = 0.0

            current_time = time.time()
            with lock:
                elapsed = current_time - thread_local.last_called
                if elapsed < min_interval:
                    time.sleep(min_interval - elapsed)
                thread_local.last_called = time.time()

            return func(*args, **kwargs)
        return wrapper
    return decorator

# set up environment variables and API client
load_dotenv('spotifyclientlogin.env')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

client_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_manager)

# function to get an artist's ID
@rate_limited(15)
def get_artist_id(name):
        result = spotify.search(q='artist:' + name, type='artist')
        items = result['artists']['items']
        if items:
            return items[0]['id']
        else:
            return None

# gets all the albums by an artist using their Spotify ID
@rate_limited(15)
def get_all_albums(id):
    album_list = []
    result = spotify.artist_albums(id, album_type='album')
    album_list.extend(result['items'])
    while result['next']:
        try:
            result = spotify.next(result)
            album_list.extend(result['items'])
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get('Retry-After', 1))
                print("Waiting due to rate limit:", retry_after)
                time.sleep(retry_after)
            else:
                raise
    return album_list

# gets all the songs where two artists worked together
@rate_limited(15)
def get_collaboration_songs(main_id, collab_id):
    album_list = get_all_albums(main_id)
    song_list = []
    # go through all albums and see if collaborating artist is on it
    for album in album_list:
        tracks = spotify.album_tracks(album['id'], limit=50)['items']
        for track in tracks:
            if any(artist['id'] == collab_id for artist in track['artists']):
                song_list.append(track['name'])
    return song_list

# finds all the artists that collaborated with a given artist
@rate_limited(15)
def get_all_collaborations(id):
    album_list = get_all_albums(id)
    collaborations = set()
    artist_cache = HashMap()
    collab_heap = Heap()

    for album in album_list:
        tracks = spotify.album_tracks(album['id'], limit=50)['items']
        for track in tracks:
            for artist in track['artists']:
                if artist['id'] != id and artist['id'] not in collaborations:
                    collaborations.add(artist['id'])
                    if not artist_cache.get(artist['id']):
                        details = spotify.artist(artist['id'])
                        artist_cache.set(artist['id'], details)

    nodes = []
    edges = []
    top_collaborators = []

    nodes.append({'id': id, 'name': spotify.artist(id)['name']})


    # for each collaborator get details from cache, find all songs, count the collabs, add to heap
    for artist_id in collaborations:
        artist = artist_cache.get(artist_id)
        if artist:
            songs = get_collaboration_songs(id, artist_id)
            unique_songs = []
            for song in songs:
                if song not in unique_songs:
                    unique_songs.append(song)
            collab_count = len(unique_songs)
            collab_heap.insert((collab_count, artist['id']))
            nodes.append({'id': artist['id'], 'name': artist['name'], 'songs': unique_songs})
            edges.append({'source': id, 'target': artist['id']})

    # extract the top 10 collaborators based on song count
    while len(top_collaborators) < 10 and not collab_heap.is_empty():
        count, artist_id = collab_heap.extract_max()
        artist = artist_cache.get(artist_id)
        if artist:
            top_collaborators.append({'name': artist['name'], 'song_count': count})

    return nodes, edges, top_collaborators
