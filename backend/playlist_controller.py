from flask import Blueprint, request, jsonify, Response
from backend import secrets
from playlist_model import get_playlists, create_playlist
import spotipy
import json

playlist = Blueprint("playlist", __name__)


@playlist.route('/get-playlists')
def get_playlist_endpoint():
    # print("Get Playlists")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']
    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()

    my_playlists = get_playlists(user, sp)

    response = jsonify(my_playlists)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@playlist.route('/create-playlist', methods=['POST'])
def create_playlist_endpoint():
    # print("Creating Playlist")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()

    req = json.loads(request.data)

    create_playlist(user, req, sp)

    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': f'{secrets.url_base}'}
    response = Response(status=200, headers=headers)

    return response
