from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlencode
import os
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

router = APIRouter(prefix='/authentication')


@router.get('/login')
def login():
    sp_oath = create_spotify_oath()
    auth_url = sp_oath.get_authorize_url()

    return RedirectResponse(auth_url, status_code=303)


@router.get('/callback')
def callback(request: Request):
    sp_oath = create_spotify_oath()
    # If access denied -> Return to landing page
    if 'error' in request.query_params.keys():
        return RedirectResponse(f"{os.getenv('url_base')}/")
    code = request.query_params['code']
    token_info = sp_oath.get_access_token(code, check_cache=False)
    response = RedirectResponse(f"{os.getenv('url_base')}/my-playlists?{urlencode(token_info)}")
    return response


@router.get('/logout')
def logout():
    return RedirectResponse(f"{os.getenv('url_base')}/")


@router.get("/refresh")
def refresh(request: Request):
    # If refresh token isn't passed -> 401
    if "refresh" not in request.headers.keys():
        print("No refresh token passed")
        return Response(status_code=401)

    refresh_token = request.headers["refresh"]
    sp_oath = create_spotify_oath()
    return sp_oath.refresh_access_token(refresh_token)


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
