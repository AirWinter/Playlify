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

# url_base = "http://localhost:8080"
# url_base = "https://playlify-app.netlify.app"
url_base = "https://playlify.net"

@app.route('/login')
def login():
    sp_oath = create_spotify_oath()
    auth_url = sp_oath.get_authorize_url()

    return redirect(auth_url)


@app.route('/callback')
def callback():
    sp_oath = create_spotify_oath()
    code = request.args.get('code')
    token_info = sp_oath.get_access_token(code, check_cache=False)
    response = redirect(f"{url_base}/playlists-view?{urlencode(token_info)}")
    return response


@app.route('/logout')
def logout():
    return redirect(f"{url_base}/")


@app.route("/refresh")
def refresh():
    print("refresh")
    # If refresh token isn't passed -> 401
    if "refresh_token" not in request.headers:
        print("No refresh token passed")
        return Response(status=401)

    refresh_token = request.headers["refresh_token"]
    sp_oath = create_spotify_oath()
    response = sp_oath.refresh_access_token(refresh_token)
    return jsonify(response)


@app.route('/songsAdded')
def songs_added():
    return 'Successfully added songs to playlist!'


@app.route('/backend/getPlaylists')
def get_playlist():
    print("Get Playlists")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']
    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()

    my_playlists = []
    count = 0
    while True:
        offset = count * 50
        playlists = sp.user_playlists(user=user['id'], limit=(offset + 50), offset=offset)
        for playlist in playlists['items']:
            image = ''
            if len(playlist['images']) > 0:
                image = playlist['images'][0]['url']
            my_playlists.append(
                {"name": playlist['name'], "description": playlist['description'], "public": playlist['public'],
                 "image": image, 'link': playlist['external_urls']['spotify'],
                 'creator': playlist['owner']['display_name']})
        count += 1
        if len(playlists) < 50:
            break
    response = jsonify(my_playlists)
    response.headers.add('Access-Control-Allow-Origin', f'{url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


# Don't actually return the songs, just store them
@app.route('/backend/getAllTracksFromLibrary', methods=['GET'])
def get_all_tracks_from_library():
    print("Get All Tracks")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)

    # Don't hardcode the market, but rather get it from the user
    user = sp.me()
    market = user['country']

    count = 0
    all_my_genres = [{'label': 'Classical', 'options': []}, {'label': 'Country', 'options': []},
                     {'label': 'EDM', 'options': []}, {'label': 'Folk', 'options': []},
                     {'label': 'Hip Hop', 'options': []}, {'label': 'Indie', 'options': []},
                     {'label': 'Jazz', 'options': []}, {'label': 'Metal', 'options': []},
                     {'label': 'K-Pop', 'options': []}, {'label': 'Pop', 'options': []},
                     {'label': 'R&B', 'options': []}, {'label': 'Trap', 'options': []},
                     {'label': 'Rap', 'options': []},
                     {'label': 'Reggaeton', 'options': []}, {'label': 'Reggae', 'options': []},
                     {'label': 'Rock', 'options': []}, {'label': 'Soul', 'options': []},
                     {'label': 'Swing', 'options': []}, {'label': 'Techno', 'options': []},
                     {'label': 'Others', 'options': []}]
    # Genres: Classical,Country,EDM,Folk,Hip Hop,House,Indie,Jazz,Metal,Pop,R&B,Rap,Reggae,Reggaeton,Rock,Soul,Swing,Techno,Trap, Others
    all_my_artists = {}
    all_my_songs = {}
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
                    all_my_artists[a_id] = {'name': a_name, 'external_url': a_url}
            song_id = items[i]['track']['id']
            song_name = items[i]['track']['name']
            date = items[i]['track']['album']['release_date']
            song_url = items[i]['track']['external_urls']['spotify']
            all_my_songs[song_id] = {'name': song_name, 'artists': artists, 'date-created': date,
                                     'external_url': song_url}

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
                genre_string = stringify(genre)
                for genre_group in all_my_genres:
                    if genre_group['label'].upper() in genre_string.upper() \
                            or genre_group['label'].upper() in genre.upper() \
                            or genre_group['label'].upper() == "OTHERS":
                        if not any(
                                genre in genre_group_values['value'] for genre_group_values in genre_group['options']):
                            genre_group['options'].append({'value': genre, 'label': genre_string})

                        break

    for song_id in all_my_songs.keys():
        song_artists_ids = all_my_songs[song_id]['artists']
        song_genres = []
        for artist_id in song_artists_ids:
            song_genres.extend(all_my_artists[artist_id]['genres'])

        all_my_songs[song_id]['genres'] = song_genres

    for genre_group in all_my_genres:
        if len(genre_group['options']) == 0:
            all_my_genres.remove(genre_group)
        else:
            label = genre_group['label']
            genre_group['label'] = "All " + label + " Genres"

    res = {'all_songs': all_my_songs, 'all_artists': all_my_artists, 'all_genres': all_my_genres}
    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', f'{url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@app.route('/backend/createPlaylist', methods=['POST'])
def create_playlist():
    print("Creating Playlist")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()

    req = json.loads(request.data)

    name = req['name']
    is_public = False  # False by default
    # If public is specified then overwrite
    if 'public' in req.keys():
        is_public = req['public']

    description = req['description']
    print(f"Description: {description}")

    # If the user provided a description
    if description is not None and description != "":
        response_create = sp.user_playlist_create(user=user['id'], name=name, public=is_public, description=description)
        if response_create['description'] is None or response_create['description'] == "":
            count = 0
            playlist_id = response_create['id']
            # Try at most 10 times to set the playlist description
            while count <= 10:
                response_update = sp.playlist_change_details(playlist_id=playlist_id, description=description)
                count += 1
                if response_update['description'] is not None and response_update['description'] != "":
                    break
    else:
        # Create empty playlist without a description
        response_create = sp.user_playlist_create(user=user['id'], name=name, public=is_public)

    print(f"Created: {response_create}")
    playlist_id = response_create['id']

    songs_to_add = json.loads(request.data)['songs_to_add']
    # print(f"Songs to add: {songs_to_add}")

    # Populate Playlist
    for list_of_songs in chunks(songs_to_add, 100):
        response_populate = sp.playlist_add_items(playlist_id, list_of_songs)
        print(f"Populated: {response_populate}")

    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': f'{url_base}'}
    response = Response(status=200, headers=headers)

    return response


@app.route('/backend/getSongsToAdd', methods=['POST'])
def get_songs_to_add():
    print("Get songs to Add")
    req = json.loads(request.data)
    filters = {"genre": req['genres'],
               "artists": req['artists'],
               "created_after_month": req['created_after_month'],
               "created_before_month": req['created_before_month']}

    all_my_songs = json.loads(req['all_my_songs'])
    all_my_artists = json.loads(req['all_my_artists'])
    songs_to_add = list(all_my_songs)

    # Apply all the filters on the songs
    for apply_filter in filters.keys():
        # Only filter if the genre filter is not 'Any'
        if apply_filter == "genre" and filters[apply_filter] is not None and filters[apply_filter] != '':
            all_genres = filters["genre"].split(";")
            if len(all_genres) > 0 and "any" not in all_genres:
                print("Filtered by genre")
                songs_to_add = list(
                    filter(lambda s: any(filter_genre in all_my_songs[s]['genres'] for filter_genre in all_genres),
                           songs_to_add))
        if apply_filter == "artists" and filters[apply_filter] is not None and filters[apply_filter] != '':
            all_artists = filters[apply_filter].split(";")
            if len(all_artists) > 0:
                print("Filtered by artists")
                songs_to_add = list(
                    filter(lambda s: any(
                        filter_artists in all_my_songs[s]['artists'].keys() for filter_artists in all_artists),
                           songs_to_add))
        elif apply_filter == "created_after_month" and filters[apply_filter] != "":
            print("Filtered by created_after_month")
            songs_to_add = list(
                filter(lambda s: all_my_songs[s]['date-created'] >= filters[apply_filter], songs_to_add))
        elif apply_filter == "created_before_month" and filters[apply_filter] != "":
            print("Filtered by created_before_month")
            songs_to_add = list(
                filter(lambda s: all_my_songs[s]['date-created'] <= filters[apply_filter], songs_to_add))

    result = {}
    for song_id in songs_to_add:
        artists = []
        for artist_id in all_my_songs[song_id]['artists'].keys():
            artists.append({'name': all_my_songs[song_id]['artists'][artist_id],
                            'external_url': all_my_artists[artist_id]['external_url']})
        # artists_string = ', '.join([str(elem) for elem in artists])
        result[song_id] = {"song_name": stringify(all_my_songs[song_id]['name']),
                           'song_url': all_my_songs[song_id]['external_url'], "artists": artists}
    return jsonify(result)


def create_spotify_oath():
    return SpotifyOAuth(
        client_id=secrets.client_id,
        client_secret=secrets.secret,
        redirect_uri=url_for('callback', _external=True),
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-private playlist-read-private playlist-read-collaborative"
    )


if __name__ == '__main__':
    app.run()
