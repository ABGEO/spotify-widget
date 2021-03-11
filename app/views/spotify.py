import json
import random
import requests

from base64 import b64encode

from flask import Blueprint, Response, render_template, request

from app import app

bp = Blueprint('spotify', __name__)


def getAuth():
    return b64encode(f"{app.config['SPOTIFY_CLIENT_ID']}:{app.config['SPOTIFY_SECRET_ID']}".encode()).decode(
        "ascii"
    )


def refreshToken():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": app.config["SPOTIFY_REFRESH_TOKEN"],
    }

    headers = {"Authorization": "Basic {}".format(getAuth())}
    response = requests.post(app.config["REFRESH_TOKEN_URL"], data=data, headers=headers)

    try:
        return response.json()["access_token"]
    except KeyError:
        print(json.dumps(response.json()))
        print("\n---\n")
        raise KeyError(str(response.json()))


def recentlyPlayed():
    token = refreshToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(app.config["RECENTLY_PLAYING_URL"], headers=headers)

    if response.status_code == 204:
        return {}
    return response.json()


def nowPlaying():
    token = refreshToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(app.config["NOW_PLAYING_URL"], headers=headers)

    if response.status_code == 204:
        return {}
    return response.json()


def barGen(barCount):
    barCSS = ""
    left = 1
    for i in range(1, barCount + 1):
        anim = random.randint(1000, 1350)
        barCSS += (
            ".bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(
                i, left, anim
            )
        )
        left += 4
    return barCSS


def loadImageB64(url):
    resposne = requests.get(url)
    return b64encode(resposne.content).decode("ascii")


def makeSVG(data, width, height):
    if data == {} or data["item"] == "None" or data["item"] is None:
        playingNow = False
        barClasses = 'bar'
        recentPlays = recentlyPlayed()
        recentPlaysLength = len(recentPlays["items"])
        itemIndex = random.randint(0, recentPlaysLength - 1)
        item = recentPlays["items"][itemIndex]["track"]
    else:
        item = data["item"]
        playingNow = True
        barClasses = 'bar barPlaying'

    barCount = 84
    contentBar = "".join([f"<div class='{barClasses}'></div>" for i in range(barCount)])
    barCSS = barGen(barCount)

    image = loadImageB64(item["album"]["images"][1]["url"])
    artistName = item["artists"][0]["name"].replace("&", "&amp;")
    songName = item["name"].replace("&", "&amp;")

    dataDict = {
        "contentBar": contentBar,
        "barCSS": barCSS,
        "artistName": artistName,
        "songName": songName,
        "image": image,
        "playingNow": playingNow,
        "width": width,
        "height": height,
    }

    return render_template("spotify.html.j2", **dataDict)


@bp.route("/")
def catch_all():
    width = request.args.get('width', '480', str)
    height = request.args.get('height', '163', str)

    data = nowPlaying()
    svg = makeSVG(data, width, height)

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp
