from auth_middleware import token_required
from flask import Blueprint, request, jsonify
from backend import secrets
from tracks_model import get_recommendations, get_tracks_to_add, get_all_tracks_from_library

tracks = Blueprint("tracks", __name__)


@tracks.route('/get-all', methods=['GET'])
@token_required
def get_all_tracks_from_library_endpoint(sp):
    user = sp.me()
    market = user['country']

    res = get_all_tracks_from_library(sp, market)

    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@tracks.route('/get-tracks-to-add', methods=['GET'])
@token_required
def get_tracks_to_add_endpoint(sp):
    user = sp.me()
    req = request.headers
    filters = {"genres": req['genres'],
               "artists": req['artists'],
               "created_after_month": req['created_after_month'],
               "created_before_month": req['created_before_month']}

    result = get_tracks_to_add(filters, user['id'])

    return jsonify(result)


@tracks.route('/get-recommendations', methods=['GET'])
@token_required
def get_recommendations_endpoint(sp):
    track_seeds_string = request.args.get('track_seeds')
    genre_seeds_string = request.args.get('genre_seeds')
    artist_seeds_string = request.args.get('artist_seeds')

    songs = get_recommendations(sp, track_seeds_string, genre_seeds_string, artist_seeds_string)

    response = jsonify(songs)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
