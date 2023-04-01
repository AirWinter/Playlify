import json

from flask import Flask, request, url_for, session, redirect, jsonify
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from secrets import id, secret, secret_key
from utils import filter_by_genre, chunks
import time

# import json

app = Flask(__name__)
app.secret_key = secret_key
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
TOKEN_INFO = "token_info"
my_genres = []
songs = []


@app.route('/home')
def home():
    return 'Welcome to Playlify'


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
    return redirect(url_for('getTracks', _external=True))


@app.route('/getTracks', methods=['GET'])
def getTracks():
    global songs
    try:
        token_info = get_token()
    except:
        print("User not logged in!")
        return redirect(url_for('login', _external=False))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter * 50, market='DE')['items']
        artists_ids = []
        song_ids = []
        dates = []
        for i in range(0, len(items)):
            song_id = items[i]['track']['id']
            song_ids.append(song_id)
            artist_id = items[i]['track']['artists'][0]['id']
            date = items[i]['track']['album']['release_date']
            dates.append(date)
            artists_ids.append(artist_id)
        artists = sp.artists(artists_ids)
        for i in range(0, len(items)):
            all_songs.append({"id": song_ids[i], "genres": artists['artists'][i]['genres'], "date-created": dates[i]})
            for genre in artists['artists'][i]['genres']:
                if genre not in my_genres:
                    my_genres.append(genre)
        iter += 1
        if len(items) < 50:
            break;
    songs = all_songs
    return jsonify(all_songs)


@app.route('/getPlaylists')
def get_playlist():
    try:
        token_info = get_token()
    except:
        print("User not logged in!")
        return redirect(url_for('login', _external=False))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.me()
    playlists = sp.user_playlists(user=user['id'], limit=50, offset=0)
    playlist_names = []
    for playlist in playlists['items']:
        playlist_names.append({"name": playlist['name']})
    return jsonify(playlist_names)


@app.route('/createPlaylist', methods=['POST'])
def create_playlist():
    global songs
    print(songs)

    if 'refresh_token' not in request.headers:
        print("Didn't pass refresh token in request header")
        return redirect(url_for('home'), 400)

    # Pass refresh token in header when calling the endpoint
    sp_oath = create_spotify_oath()
    token_info = sp_oath.refresh_access_token(request.headers['refresh_token'])

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.me()

    name = json.loads(request.data)['name']
    isPublic = json.loads(request.data)['public']


    genre = json.loads(request.data)['genre']

    # Create empty playlist
    response_create = sp.user_playlist_create(user=user['id'], name=name, public=isPublic)

    print(f"Created: {response_create}")
    playlist_id = response_create['id']

    if 'description' in json.loads(request.data).keys():
        description = json.loads(request.data)['description']
        print(f"Description: {description}")
        response_change = sp.playlist_change_details(playlist_id=playlist_id, description=description)
        print(response_change)


    # Populate Playlist
    # Note if there are more than 100 songs to add then do chunks
    songs_to_add = filter_by_genre(genre, songs)
    print(songs_to_add)
    for list_of_songs in chunks(songs_to_add, 100):
        response_populate = sp.playlist_add_items(playlist_id, list_of_songs)
        print(f"Populated: {response_populate}")

    return redirect(url_for('home'), 200)


@app.route('/logout')
def logout():
    if session.get(TOKEN_INFO, None) is None:
        print("Already logged out")
    else:
        session.clear()
        print("User logged out!")
    return redirect(url_for('home', _external=False), 200)


def get_token():
    token_info = session.get(TOKEN_INFO, None)

    if token_info is None:
        raise Exception("There is no session token!")

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oath = create_spotify_oath()
        token_info = sp_oath.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oath():
    return SpotifyOAuth(
        client_id=id,
        client_secret=secret,
        redirect_uri=url_for('callback', _external=True),
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-private playlist-read-private"
    )


if __name__ == '__main__':
    app.run()
