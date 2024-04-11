from flask import Flask
from flask_cors import CORS
from authentication_controller import authentication
from playlist_controller import playlist
from tracks_controller import tracks
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")
app.register_blueprint(authentication, url_prefix="/authentication")
app.register_blueprint(playlist, url_prefix="/playlist")
app.register_blueprint(tracks, url_prefix="/tracks")

CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
