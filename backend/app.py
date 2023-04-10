from flask import Flask, request, url_for, session, redirect, jsonify, abort, Response
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
from backend import secrets
from utils import chunks, stringify
import time
import spotipy
import json

app = Flask(__name__)
app.secret_key = secrets.secret_key
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

# CORS(app, resources={r"/*": {'origins': "*"}})
CORS(app, resources={r'/*':{'origins': 'http://localhost:8080',"allow_headers": "Access-Control-Allow-Origin"}})
CORS(app, supports_credentials=True)
# app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

TOKEN_INFO = "token_info"
all_my_genres = {}
all_my_artists = {}
all_my_songs = {}
loaded = False

@app.route('/login')
def login():
    sp_oath = create_spotify_oath()
    auth_url = sp_oath.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    sp_oath = create_spotify_oath()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oath.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect("http://localhost:8080/my-playlists")


@app.route('/logout')
def logout():
    if session.get(TOKEN_INFO, None) is None:
        print("Already logged out")
    else:
        session.clear()
        print("User logged out!")
    return redirect("http://localhost:8080/")


@app.route('/songsAdded')
def songs_added():
    return 'Successfully added songs to playlist!'


@app.route('/backend/getPlaylists')
def get_playlist():
    try:
        token_info = get_token()
    except NotLoggedInException:
        print("User not logged in!")
        headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': 'http://localhost:8080'}
        response = Response(status=400, headers=headers)
        return response

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.me()
    playlists = sp.user_playlists(user=user['id'], limit=50, offset=0)
    my_playlists = []
    for playlist in playlists['items']:
        my_playlists.append(
            {"name": playlist['name'], "description": playlist['description'], "public": playlist['public']})

    response = jsonify(my_playlists)
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


# @app.route('/backend/getAllTracksFromLibrary', methods=['GET'])
# def get_all_tracks_from_library():
#     global songs
#     if 'refresh_token' not in request.headers:
#         print("Didn't pass refresh token in request header")
#         return redirect(url_for('home'), 400)
#
#     sp_oath = create_spotify_oath()
#     token_info = sp_oath.refresh_access_token(request.headers['refresh_token'])
#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     all_songs = []
#     count = 0
#     while True:
#         items = sp.current_user_saved_tracks(limit=50, offset=count * 50, market='DE')['items']
#         artists_ids = []
#         song_ids = []
#         dates = []
#         for i in range(0, len(items)):
#             song_id = items[i]['track']['id']
#             song_ids.append(song_id)
#             artist_id = items[i]['track']['artists'][0]['id']
#             date = items[i]['track']['album']['release_date']
#             dates.append(date)
#             artists_ids.append(artist_id)
#         artists = sp.artists(artists_ids)
#         for i in range(0, len(items)):
#             all_songs.append({"id": song_ids[i], "genres": artists['artists'][i]['genres'], "date-created": dates[i]})
#             for genre in artists['artists'][i]['genres']:
#                 if genre not in all_my_genres.keys():
#                     all_my_genres[genre] = stringify(genre)
#         count += 1
#         if len(items) < 50:
#             break
#     songs = all_songs
#     response = jsonify(all_songs)
#     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     return response

# Don't actually return the songs, just store them
@app.route('/backend/loadAllTracksFromLibrary', methods=['GET'])
def load_all_tracks_from_library():
    global loaded
    try:
        token_info = get_token()
    except NotLoggedInException:
        print("User not logged in!")
        return redirect(url_for('login', _external=False))

    if loaded:
        headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': 'http://localhost:8080'}
        response = Response(status=200, headers=headers)
        return response

    sp = spotipy.Spotify(auth=token_info['access_token'])

    count = 0
    # Don't hardcode the market, but rather get it from the user
    user = sp.me()
    market = user['country']
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=count * 50, market=market)['items']
        for i in range(0, len(items)):
            number_of_artists = len(items[i]['track']['artists'])
            artists = {}
            for j in range(0, number_of_artists):
                a_id = items[i]['track']['artists'][j]['id']
                a_name = items[i]['track']['artists'][j]['name']
                artists[a_id] = a_name
                if a_id not in all_my_artists.keys():
                    all_my_artists[a_id] = {'name': a_name}
            song_id = items[i]['track']['id']
            song_name = items[i]['track']['name']
            date = items[i]['track']['album']['release_date']
            all_my_songs[song_id] = {'name': song_name, 'artists': artists, 'date-created': date}

        count += 1
        if len(items) < 50:
            break

    for chunks_of_artist_ids in chunks(list(all_my_artists.keys()), 50):
        artists_information = sp.artists(chunks_of_artist_ids)
        for artist_information in artists_information['artists']:
            artist_id = artist_information['id']
            genres = artist_information['genres']
            all_my_artists[artist_id]['genres'] = genres
            for genre in genres:
                if genre not in all_my_genres.keys():
                    all_my_genres[genre] = stringify(genre)

    for song_id in all_my_songs.keys():
        song_artists_ids = all_my_songs[song_id]['artists']
        song_genres = []
        for artist_id in song_artists_ids:
            song_genres.extend(all_my_artists[artist_id]['genres'])

        all_my_songs[song_id]['genres'] = song_genres

    loaded = True
    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': 'http://localhost:8080'}
    response = Response(status=200, headers=headers)
    # print(all_my_songs)
    return response


# In case they add genres to songs
# @app.route('/backend/getAllTracks', methods=['GET'])
# def get_all_tracks():
#     global songs
#     try:
#         token_info = get_token()
#     except NotLoggedInException:
#         print("User not logged in!")
#         return redirect(url_for('login', _external=False))
#
#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     all_songs = []
#     count = 0
#     user = sp.me()
#     market = user['country']
#     while True:
#         items = sp.current_user_saved_tracks(limit=50, offset=count * 50, market=market)['items']
#
#         for i in range(0, len(items)):
#             song_id = items[i]['track']['id']
#             genres = items[i]['genres']
#             artist_id = items[i]['track']['artists'][0]['id']
#             date = items[i]['track']['album']['release_date']
#             all_songs.append({"id": song_id, "artist_id" : artist_id, "genres": genres, "date-created": date})
#         count += 1
#         if len(items) < 50:
#             break
#     songs = all_songs
#     return jsonify(all_songs)


@app.route('/backend/createPlaylist', methods=['POST'])
def create_playlist():
    try:
        token_info = get_token()
    except NotLoggedInException:
        print("User not logged in!")
        return redirect(url_for('login', _external=False))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.me()

    name = json.loads(request.data)['name']
    is_public = False  # False by default
    # If public is specified then overwrite
    if 'public' in json.loads(request.data).keys():
        is_public = json.loads(request.data)['public']

    description = json.loads(request.data)['description']
    print(f"Description: {description}")
    # Create empty playlist
    response_create = sp.user_playlist_create(user=user['id'], name=name, description=description, public=is_public)

    print(f"Created: {response_create}")
    playlist_id = response_create['id']

    if 'description' in json.loads(request.data).keys():
        description = json.loads(request.data)['description']
        if len(description) > 0:
            response_change = sp.playlist_change_details(playlist_id=playlist_id, description=description)
            print(f"Changed: {response_change}")

    songs_to_add = json.loads(request.data)['songs_to_add']
    print(f"Songs to add: {songs_to_add}")

    # Populate Playlist
    for list_of_songs in chunks(songs_to_add, 100):
        response_populate = sp.playlist_add_items(playlist_id, list_of_songs)
        print(f"Populated: {response_populate}")

    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': 'http://localhost:8080'}
    response = Response(status=200, headers=headers)

    return response


@app.route('/backend/getSongsToAdd', methods=['GET'])
def get_songs_to_add():
    filters = {"genre": request.args.get('genres'),
               "artists": request.args.get('artists'),
               "created_after_month": request.args.get('created_after_month'),
               "created_before_month": request.args.get('created_before_month')}
    songs_to_add = list(all_my_songs)
    # Apply all the filters on the songs
    for apply_filter in filters.keys():
        # Only filter if the genre filter is not 'Any'
        if apply_filter == "genre" and filters[apply_filter] is not None:
            all_genres = filters["genre"].split(";")
            if len(all_genres) > 0 and "any" not in all_genres:
                songs_to_add = list(filter(lambda s: any(filter_genre in all_my_songs[s]['genres'] for filter_genre in all_genres), songs_to_add))
        if apply_filter == "artists" and filters[apply_filter] is not None:
            all_artists = filters[apply_filter].split(";")
            if len(all_artists) > 0:
                songs_to_add = list(
                    filter(lambda s: any(filter_artists in all_my_songs[s]['artists'].keys() for filter_artists in all_artists), songs_to_add))
        elif apply_filter == "created_after_month" and filters[apply_filter] != "":
            songs_to_add = list(filter(lambda s: all_my_songs[s]['date-created'] >= filters[apply_filter], songs_to_add))
        elif apply_filter == "created_before_month" and filters[apply_filter] != "":
            songs_to_add = list(filter(lambda s: all_my_songs[s]['date-created'] <= filters[apply_filter], songs_to_add))

    # print(f"Songs to add: {songs_to_add}")
    result = {}
    for song_id in songs_to_add:
        artists = []
        for artist_id in all_my_songs[song_id]['artists'].keys():
            artists.append(all_my_songs[song_id]['artists'][artist_id])
        artists_string = ', '.join([str(elem) for elem in artists])
        result[song_id] = {"song_name": stringify(all_my_songs[song_id]['name']), "artists": artists_string}
    print(result)
    return jsonify(result)


@app.route('/backend/getAllMyGenres', methods=['GET'])
def get_all_my_genres():
    return all_my_genres


@app.route('/backend/getAllMyArtists', methods=['GET'])
def get_all_my_artists():
    artists_to_return = {}
    for artist_id in all_my_artists.keys():
        artists_to_return[artist_id] = all_my_artists[artist_id]['name']

    return artists_to_return


class NotLoggedInException(Exception):
    """Raised when user is not logged in"""
    pass


def get_token():
    token_info = session.get(TOKEN_INFO, None)

    if token_info is None:
        raise NotLoggedInException("There is no session token!")

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oath = create_spotify_oath()
        token_info = sp_oath.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oath():
    return SpotifyOAuth(
        client_id=secrets.client_id,
        client_secret=secrets.secret,
        redirect_uri=url_for('callback', _external=True),
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-private playlist-read-private"
    )


if __name__ == '__main__':
    app.run()
