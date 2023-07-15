from flask import Blueprint, request, jsonify, Response
from backend import secrets
from utils import chunks, stringify
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
def get_tracks_to_add():
    # print("Get songs to Add")
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
                # print("Filtered by genre")
                songs_to_add = list(
                    filter(lambda s: any(filter_genre in all_my_songs[s]['genres'] for filter_genre in all_genres),
                           songs_to_add))
        if apply_filter == "artists" and filters[apply_filter] is not None and filters[apply_filter] != '':
            all_artists = filters[apply_filter].split(";")
            if len(all_artists) > 0:
                # print("Filtered by artists")
                songs_to_add = list(
                    filter(lambda s: any(
                        filter_artists in all_my_songs[s]['artists'].keys() for filter_artists in all_artists),
                           songs_to_add))
        elif apply_filter == "created_after_month" and filters[apply_filter] != "":
            # print("Filtered by created_after_month")
            songs_to_add = list(
                filter(lambda s: all_my_songs[s]['date-created'] >= filters[apply_filter], songs_to_add))
        elif apply_filter == "created_before_month" and filters[apply_filter] != "":
            # print("Filtered by created_before_month")
            songs_to_add = list(
                filter(lambda s: all_my_songs[s]['date-created'] <= filters[apply_filter], songs_to_add))

    result = {}
    for song_id in songs_to_add:
        artists = []
        for artist_id in all_my_songs[song_id]['artists'].keys():
            artists.append({'name': all_my_songs[song_id]['artists'][artist_id],
                            'external_url': all_my_artists[artist_id]['external_url']})
        result[song_id] = {"song_name": stringify(all_my_songs[song_id]['name']),
                           'song_url': all_my_songs[song_id]['external_url'], "artists": artists,
                           'preview_url': all_my_songs[song_id]['preview_url']}
    return jsonify(result)


@tracks.route('/get-recommendations', methods=['GET'])
def get_recommendations():
    # print("Get Recommendations")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)

    N = 10
    number_of_seeds = 0

    track_seeds_string = request.args.get('track_seeds')
    if track_seeds_string is not None and len(track_seeds_string) > 0:
        track_seeds_array = track_seeds_string.split(";")
        num = min(5, len(track_seeds_array))
        track_seeds = track_seeds_array[0:num]
        number_of_seeds += len(track_seeds)
    else:
        track_seeds = None

    genre_seeds_string = request.args.get('genre_seeds')
    if number_of_seeds < 5 and genre_seeds_string is not None and len(genre_seeds_string) > 0:
        genre_seeds_array = genre_seeds_string.split(";")
        num = min(5 - number_of_seeds, len(genre_seeds_array))
        genre_seeds = genre_seeds_array[0:num]
        number_of_seeds += len(genre_seeds)
    else:
        genre_seeds = None

    # print(genre_seeds)

    artist_seeds_string = request.args.get('artist_seeds')
    if number_of_seeds < 5 and artist_seeds_string is not None and len(artist_seeds_string) > 0:
        artist_seeds_array = artist_seeds_string.split(";")
        num = min(5 - number_of_seeds, len(artist_seeds_array))
        artist_seeds = artist_seeds_array[0:num]
        number_of_seeds += len(artist_seeds)
    else:
        artist_seeds = None

    songs = {}
    recommendations = sp.recommendations(seed_genres=genre_seeds, seed_artists=artist_seeds, seed_tracks=track_seeds,
                                         limit=N)
    # print(recommendations)
    for track in recommendations['tracks']:
        track_name = track['name']
        track_id = track['id']
        track_url = track['external_urls']['spotify']
        track_date = track['album']['release_date']
        preview_url = track['preview_url']
        artists = track['artists']
        track_artists = []
        for artist in artists:
            artist_name = artist['name']
            artist_url = artist['external_urls']['spotify']
            track_artists.append({'external_url': artist_url, 'name': artist_name})

        songs[track_id] = {'artists': track_artists, 'date-created': track_date, 'song_url': track_url,
                           'song_name': track_name, 'preview_url': preview_url}

    response = jsonify(songs)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
