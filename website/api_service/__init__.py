import os


API_KEY = os.getenv("API_KEY", "YOUR_API_KEY_HERE")
TRACK_SEARCH_BASE_URL = "http://api.musixmatch.com/ws/1.1/track.search?q="
TRACK_GET_BASE_URL = "http://api.musixmatch.com/ws/1.1/track.get?commontrack_id="
