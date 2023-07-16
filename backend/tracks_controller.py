from flask import Blueprint, request, jsonify, Response
from backend import secrets
from utils import chunks, stringify
from tracks_model import get_recommendations, get_tracks_to_add
import spotipy
import json

tracks = Blueprint("tracks", __name__)


@tracks.route('/get-all', methods=['GET'])
def get_all_tracks_from_library():
    # print("Get All Tracks")
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
        track_array = list(map(lambda i: i['track'], items))
        for track in track_array:
            artists = {}
            for artist in track['artists']:
                a_id = artist['id']
                a_name = artist['name']
                a_url = artist['external_urls']['spotify']
                artists[a_id] = a_name
                if a_id not in all_my_artists.keys():
                    all_my_artists[a_id] = {'name': a_name, 'external_url': a_url}
            song_id = track['id']
            song_name = track['name']
            date = track['album']['release_date']
            song_url = track['external_urls']['spotify']
            preview_url = track['preview_url']
            all_my_songs[song_id] = {'name': song_name, 'artists': artists, 'date-created': date,
                                     'external_url': song_url, 'preview_url': preview_url}

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
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@tracks.route('/get-tracks-to-add', methods=['POST'])
def get_tracks_to_add_endpoint():
    # print("Get songs to Add")
    req = json.loads(request.data)
    filters = {"genres": req['genres'],
               "artists": req['artists'],
               "created_after_month": req['created_after_month'],
               "created_before_month": req['created_before_month']}

    all_my_songs = json.loads(req['all_my_songs'])
    all_my_artists = json.loads(req['all_my_artists'])

    result = get_tracks_to_add(filters, all_my_songs, all_my_artists)

    return jsonify(result)


@tracks.route('/get-recommendations', methods=['GET'])
def get_recommendations_endpoint():
    # print("Get Recommendations")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)

    track_seeds_string = request.args.get('track_seeds')
    genre_seeds_string = request.args.get('genre_seeds')
    artist_seeds_string = request.args.get('artist_seeds')

    songs = get_recommendations(sp, track_seeds_string, genre_seeds_string, artist_seeds_string)

    response = jsonify(songs)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
