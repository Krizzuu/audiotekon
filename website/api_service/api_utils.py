from . import API_KEY, TRACK_SEARCH_BASE_URL, TRACK_GET_BASE_URL
import json
import requests
from munch import DefaultMunch


def get_tracks(keywords: str):
    if API_KEY == "YOUR_API_KEY_HERE":
        raise ValueError("Invalid API provided")
    url = TRACK_SEARCH_BASE_URL + keywords + f"&apikey={API_KEY}&s_track_rating=desc"
    response = requests.get(url)
    content = json.loads(response.content.decode())
    if content['message']['header']['status_code'] != 200:
        return None
    # tracks = content['message']['body']['track_list']
    tracks = DefaultMunch.fromDict(content['message']['body']['track_list'])
    tracks = [track.track for track in tracks]
    return tracks

def get_track(id):
    if API_KEY == "YOUR_API_KEY_HERE":
        raise ValueError("Invalid API provided")
    url = TRACK_GET_BASE_URL + id + f"&apikey={API_KEY}"
    response = requests.get(url)
    content = json.loads(response.content.decode())
    if content['message']['header']['status_code'] != 200:
        return None
    track = DefaultMunch.fromDict(content['message']['body']['track'])
    return track
