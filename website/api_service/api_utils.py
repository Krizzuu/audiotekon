from . import API_KEY, TRACK_BASE_URL
import json
import requests
from munch import DefaultMunch


def get_tracks(keywords: str):
    url = TRACK_BASE_URL + keywords + f"&apikey={API_KEY}&s_track_rating=desc"
    response = requests.get(url)
    content = json.loads(response.content.decode())
    if content['message']['header']['status_code'] != 200:
        return None
    # tracks = content['message']['body']['track_list']
    tracks = DefaultMunch.fromDict(content['message']['body']['track_list'])
    tracks = [track.track for track in tracks]
    return tracks


