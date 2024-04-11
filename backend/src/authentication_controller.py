from flask import Blueprint, request, redirect, jsonify, Response
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlencode
import os

authentication = Blueprint("authentication", __name__)


@authentication.route('/login')
def login():
    sp_oath = create_spotify_oath()
    auth_url = sp_oath.get_authorize_url()

    return redirect(auth_url)


@authentication.route('/callback')
def callback():
    sp_oath = create_spotify_oath()
    # If access denied -> Return to landing page
    if 'error' in request.args.keys():
        return redirect(f"{os.getenv('url_base')}/")
    code = request.args.get('code')
    token_info = sp_oath.get_access_token(code, check_cache=False)
    response = redirect(f"{os.getenv('url_base')}/my-playlists?{urlencode(token_info)}")
    return response


@authentication.route('/logout')
def logout():
    return redirect(f"{os.getenv('url_base')}/")


@authentication.route("/refresh", methods=['GET'])
def refresh():
    # print("refresh")
    # If refresh token isn't passed -> 401
    if "RefreshToken" not in request.headers:
        print("No refresh token passed")
        return Response(status=401)

    refresh_token = request.headers["RefreshToken"]
    sp_oath = create_spotify_oath()
    response = sp_oath.refresh_access_token(refresh_token)
    return jsonify(response)


def create_spotify_oath():
    redirect_uri = os.getenv('url_backend')
    client_id = os.getenv("client_id")
    client_secret = os.getenv("secret")
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=f"{redirect_uri}/authentication/callback",
        show_dialog=True,  # Show permission screen every time
        scope="user-library-read playlist-modify-public playlist-modify-private user-read-private playlist-read-private playlist-read-collaborative"
    )
