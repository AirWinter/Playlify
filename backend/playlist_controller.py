from auth_middleware import token_required
from flask import Blueprint, request, jsonify, Response
from backend import secrets
from playlist_model import get_playlists, create_playlist
import json

playlist = Blueprint("playlist", __name__)


@playlist.route('/get-playlists')
@token_required
def get_playlist_endpoint(sp):
    user = sp.me()

    my_playlists = get_playlists(user['id'], sp)

    response = jsonify(my_playlists)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@playlist.route('/create-playlist', methods=['POST'])
@token_required
def create_playlist_endpoint(sp):
    user = sp.me()

    req = json.loads(request.data)

    create_playlist(user['id'], req, sp)

    headers = {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': f'{secrets.url_base}'}
    response = Response(status=200, headers=headers)

    return response
