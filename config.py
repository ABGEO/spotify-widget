import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'

    SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIFY_SECRET_ID = os.environ["SPOTIFY_SECRET_ID"]
    SPOTIFY_REFRESH_TOKEN = os.environ["SPOTIFY_REFRESH_TOKEN"]

    REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
    RECENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/recently-played?limit=10"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


del os
