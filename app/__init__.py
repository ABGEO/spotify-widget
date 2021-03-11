import os

from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

from app.views import spotify

app.register_blueprint(spotify.bp)
