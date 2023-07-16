from utils import stringify


def get_tracks_to_add(filters, all_my_songs, all_my_artists):
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
            artists.append({'name': all_my_songs[song_id]['artists'][artist_id],
                            'external_url': all_my_artists[artist_id]['external_url']})
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
