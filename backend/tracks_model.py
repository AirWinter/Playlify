from utils import stringify, chunks
import mongodb_repository

def get_all_tracks_from_library(sp, market):
    count = 0
    # Hard-coded genre groups
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
                artists[a_id] = {'name': a_name, 'external_url': a_url}
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
        song_artists_ids = all_my_songs[song_id]['artists'].keys()
        song_genres = set()
        for artist_id in song_artists_ids:
            for g in all_my_artists[artist_id]['genres']:
                song_genres.add(g)

        all_my_songs[song_id]['genres'] = list(song_genres)

    for genre_group in all_my_genres:
        if len(genre_group['options']) == 0:
            all_my_genres.remove(genre_group)
        else:
            label = genre_group['label']
            genre_group['label'] = "All " + label + " Genres"

    artist_options = {}
    for a_id in all_my_artists.keys():
        artist_options[a_id] = all_my_artists[a_id]['name']
    user = sp.me()
    mongodb_repository.write_to_db(user['id'], all_my_songs)
    res = {'artist_options': artist_options, 'all_genres': all_my_genres}
    return res


def get_tracks_to_add(filters, user_id: str):
    all_my_songs = mongodb_repository.get_by_user_id(user_id)
    songs_to_add = list(all_my_songs)
    # Apply all the filters on the songs
    for apply_filter in filters.keys():
        # Only filter if the genre filter is not 'Any'
        if apply_filter == "genres" and filters[apply_filter] is not None and filters[apply_filter] != '':
            all_genres = filters["genres"].split(";")
            if len(all_genres) > 0 and "any" not in all_genres:
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
            artists.append({'name': all_my_songs[song_id]['artists'][artist_id]['name'],
                            'external_url': all_my_songs[song_id]['artists'][artist_id]['external_url']})
        result[song_id] = {"song_name": stringify(all_my_songs[song_id]['name']),
                           'song_url': all_my_songs[song_id]['external_url'], "artists": artists,
                           'preview_url': all_my_songs[song_id]['preview_url']}

    return result


def get_recommendations(sp, track_seeds_string, genre_seeds_string, artist_seeds_string):
    N = 10
    number_of_seeds = 0

    if track_seeds_string is not None and len(track_seeds_string) > 0:
        track_seeds_array = track_seeds_string.split(";")
        num = min(5, len(track_seeds_array))
        track_seeds = track_seeds_array[0:num]
        number_of_seeds += len(track_seeds)
    else:
        track_seeds = None

    if number_of_seeds < 5 and genre_seeds_string is not None and len(genre_seeds_string) > 0:
        genre_seeds_array = genre_seeds_string.split(";")
        num = min(5 - number_of_seeds, len(genre_seeds_array))
        genre_seeds = genre_seeds_array[0:num]
        number_of_seeds += len(genre_seeds)
    else:
        genre_seeds = None

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
    if 'tracks' in recommendations.keys():
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

    return songs
