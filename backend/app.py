from flask import Flask
from flask_cors import CORS
from backend import secrets
from authentication_controller import authentication
from playlist_controller import playlist
from tracks_controller import tracks

app = Flask(__name__)
app.secret_key = secrets.secret_key
app.register_blueprint(authentication, url_prefix="/authentication")
app.register_blueprint(playlist, url_prefix="/playlist")
app.register_blueprint(tracks, url_prefix="/tracks")

CORS(app)

if __name__ == '__main__':
    app.run()
