from flask import Blueprint, request, jsonify, Response
from backend import secrets
from utils import chunks
import spotipy
import json

playlist = Blueprint("playlist", __name__)


@playlist.route('/get-playlists')
def get_playlist():
    # print("Get Playlists")
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
                 "imageUrl": image, 'link': playlist['external_urls']['spotify'],
                 'creator': playlist['owner']['display_name']})
        count += 1
        if len(playlists) < 50:
            break
    response = jsonify(my_playlists)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@playlist.route('/create-playlist', methods=['POST'])
def create_playlist():
    # print("Creating Playlist")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()

    req = json.loads(request.data)

    name = req['name']
    display_on_profile = False  # False by default
    # If public is specified then overwrite
    if 'display' in req.keys():
        display_on_profile = req['display']

    description = req['description']

    # If the user provided a description
    if description is not None and description != "":
        response_create = sp.user_playlist_create(user=user['id'], name=name, public=display_on_profile,
                                                  description=description)
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
        response_create = sp.user_playlist_create(user=user['id'], name=name, public=display_on_profile)

    playlist_id = response_create['id']

    songs_to_add_string = req['songs_to_add']
    songs_to_add = songs_to_add_string.split(",")
    # print(f"Songs to add: {songs_to_add}")

    # Populate Playlist
    for list_of_songs in chunks(songs_to_add, 100):
        sp.playlist_add_items(playlist_id, list_of_songs)
        # print(f"Populated: {response_populate}")

    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': f'{secrets.url_base}'}
    response = Response(status=200, headers=headers)

    return response
