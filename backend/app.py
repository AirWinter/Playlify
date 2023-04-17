from flask import Flask, request, url_for, redirect, jsonify, Response
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth
from backend import secrets
from utils import chunks, stringify
from urllib.parse import urlencode
import spotipy
import json

app = Flask(__name__)
app.secret_key = secrets.secret_key

CORS(app)

all_my_genres = {}
all_my_artists = {}
all_my_songs = {}

url_base = "http://localhost:8080"
# url_base = "https://playlify-app.netlify.app"
# url_base = "https://playlify.net"

@app.route('/login')
def login():
    global all_my_genres
    global all_my_artists
    global all_my_songs

    sp_oath = create_spotify_oath()
    auth_url = sp_oath.get_authorize_url()

    all_my_genres = {}
    all_my_artists = {}
    all_my_songs = {}
    return redirect(auth_url)


@app.route('/callback')
def callback():
    sp_oath = create_spotify_oath()
    code = request.args.get('code')
    token_info = sp_oath.get_access_token(code, check_cache=False)
    response = redirect(f"{url_base}/my-playlists?{urlencode(token_info)}")
    return response


@app.route('/logout')
def logout():
    global all_my_genres
    global all_my_artists
    global all_my_songs

    all_my_genres = {}
    all_my_artists = {}
    all_my_songs = {}
    return redirect(f"{url_base}/")


@app.route("/refresh")
def refresh():
    # If refresh token isn't passed -> 400
    if "refresh_token" not in request.headers:
        print("No refresh token passed")
        return Response(status=400)

    refresh_token = request.headers["refresh_token"]
    print(refresh_token)
    sp_oath = create_spotify_oath()
    response = sp_oath.refresh_access_token(refresh_token)
    return jsonify(response)


@app.route('/songsAdded')
def songs_added():
    return 'Successfully added songs to playlist!'


@app.route('/backend/getPlaylists')
def get_playlist():
    print("Get Playlist")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=400)

    access_token = request.headers['Token']
    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()
    # TODO: What if they have more than 50 playlists?
    playlists = sp.user_playlists(user=user['id'], limit=50, offset=0)
    my_playlists = []
    for playlist in playlists['items']:
        my_playlists.append(
            {"name": playlist['name'], "description": playlist['description'], "public": playlist['public']})

    response = jsonify(my_playlists)
    response.headers.add('Access-Control-Allow-Origin', f'{url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    print(response.headers)
    return response


# Don't actually return the songs, just store them
@app.route('/backend/loadAllTracksFromLibrary', methods=['GET'])
def load_all_tracks_from_library():
    global all_my_genres
    global all_my_artists
    global all_my_songs
    all_my_genres = {}
    all_my_artists = {}
    all_my_songs = {}
    print("Load All Tracks")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=400)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)

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
                a_url = items[i]['track']['artists'][j]['external_urls']['spotify']
                artists[a_id] = a_name
                if a_id not in all_my_artists.keys():
                    all_my_artists[a_id] = {'name': a_name, 'external_url' : a_url}
            song_id = items[i]['track']['id']
            song_name = items[i]['track']['name']
            date = items[i]['track']['album']['release_date']
            song_url = items[i]['track']['external_urls']['spotify']
            all_my_songs[song_id] = {'name': song_name, 'artists': artists, 'date-created': date, 'external_url': song_url}

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

    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': f'{url_base}'}
    response = Response(status=200, headers=headers)
    return response


@app.route('/backend/createPlaylist', methods=['POST'])
def create_playlist():
    print("Creating Playlist")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=400)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()

    name = json.loads(request.data)['name']
    is_public = False  # False by default
    # If public is specified then overwrite
    if 'public' in json.loads(request.data).keys():
        is_public = json.loads(request.data)['public']

    description = json.loads(request.data)['description']
    print(f"Description: {description}")

    # Create empty playlist
    response_create = sp.user_playlist_create(user=user['id'], name=name, public=is_public, description=description)

    print(f"Created: {response_create}")
    playlist_id = response_create['id']

    songs_to_add = json.loads(request.data)['songs_to_add']
    print(f"Songs to add: {songs_to_add}")

    # Populate Playlist
    for list_of_songs in chunks(songs_to_add, 100):
        response_populate = sp.playlist_add_items(playlist_id, list_of_songs)
        print(f"Populated: {response_populate}")

    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': f'{url_base}'}
    response = Response(status=200, headers=headers)

    return response


@app.route('/backend/getSongsToAdd', methods=['GET'])
def get_songs_to_add():
    print("Get songs to Add")
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

    result = {}
    for song_id in songs_to_add:
        artists = []
        for artist_id in all_my_songs[song_id]['artists'].keys():
            artists.append({'name': all_my_songs[song_id]['artists'][artist_id], 'external_url': all_my_artists[artist_id]['external_url']})
        # artists_string = ', '.join([str(elem) for elem in artists])
        result[song_id] = {"song_name": stringify(all_my_songs[song_id]['name']), 'song_url': all_my_songs[song_id]['external_url'], "artists": artists}
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


def create_spotify_oath():
    return SpotifyOAuth(
        client_id=secrets.client_id,
        client_secret=secrets.secret,
        redirect_uri=url_for('callback', _external=True),
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-private playlist-read-private playlist-read-collaborative"
    )


if __name__ == '__main__':
    app.run()
