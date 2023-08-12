from flask import Blueprint, request, jsonify, Response
from backend import secrets
from tracks_model import get_recommendations, get_tracks_to_add, get_all_tracks_from_library
import spotipy
import json

tracks = Blueprint("tracks", __name__)


@tracks.route('/get-all', methods=['GET'])
def get_all_tracks_from_library_endpoint():
    # print("Get All Tracks")
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']

    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()
    market = user['country']

    res = get_all_tracks_from_library(sp, market)

    response = jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', f'{secrets.url_base}')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@tracks.route('/get-tracks-to-add', methods=['POST'])
def get_tracks_to_add_endpoint():
    # print("Get songs to Add")
    req = json.loads(request.data)
    if 'Token' not in request.headers:
        print("No Token Passed")
        return Response(status=401)

    access_token = request.headers['Token']
    sp = spotipy.Spotify(auth=access_token)
    user = sp.me()

    filters = {"genres": req['genres'],
               "artists": req['artists'],
               "created_after_month": req['created_after_month'],
               "created_before_month": req['created_before_month']}

    result = get_tracks_to_add(filters, user['id'])

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
