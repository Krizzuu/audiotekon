from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flask_login import login_required, current_user

from website import redis_client, db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@login_required
@views.route("/library")
def show_library():
    return render_template('library.html', user=current_user)


@login_required
@views.route('/search', methods=['POST'])
def search():
    query = request.form['query']

    # Perform API search here, get the results
    from website.api_service.api_utils import get_tracks
    search_results = get_tracks(query)
    # search_results = []
    # Render the search results
    return render_template('search_songs.html', search_results=search_results)

@login_required
@views.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    # Get the song from the database
    song_id = request.form['track_id']
    name = request.form['name']
    artist = request.form['artist']
    has_lyrics = request.form['has_lyrics']
    from website.models import Song
    song = Song.query.get(song_id)

    if current_user.playlist is None:
        # Create a new playlist for the user
        from website.models import Playlist
        current_user.playlist = Playlist(user_id=current_user.id)
        db.session.add(current_user.playlist)

    if not song and song_id:
        new_song = Song(id=song_id, name=name, artist=artist, has_lyrics=int(has_lyrics)!=0)
        db.session.add(new_song)

    # Add the song to the user's playlist
    current_user.playlist.songs.append(new_song)
    db.session.commit()

    flash('Song added to playlist.', 'success')
    return redirect(url_for('views.show_library'))
