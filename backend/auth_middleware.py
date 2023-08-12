from functools import wraps
from flask import request, Response
import spotipy


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Token" not in request.headers or request.headers["Token"] == "":
            return Response(status=401)

        token = request.headers["Token"]
        sp = spotipy.Spotify(auth=token)
        return f(sp, *args, **kwargs)

    return decorated
