from auth_middleware import token_required
from flask import Blueprint, request, jsonify, Response
from backend import secrets
from tracks_model import get_recommendations, get_tracks_to_add, get_all_tracks_from_library
import json

tracks = Blueprint("tracks", __name__)


@tracks.route('/get-all', methods=['GET'])
@token_required
def get_all_tracks_from_library_endpoint(sp):
    res = get_all_tracks_from_library(sp)
    if len(res['all_songs']) == 0:
        print("User doesn't have any tracks saved")
        return Response(status=204)

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
