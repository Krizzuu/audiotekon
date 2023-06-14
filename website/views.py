from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from website import redis_client, db, add_if_doesnt_exist

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@login_required
@views.route("/library")
def library():
    return render_template('library.html', user=current_user)


@login_required
@views.route('/search', methods=['POST'])
def search():
    query = request.form['query']

    # Perform API search here, get the results
    from website.api_service.api_utils import get_tracks
    import json
    from threading import Thread
    try:
        search_results = get_tracks(query)
        for track in search_results:
            th = Thread(target=redis_client.set, args=(track.track_id, json.dumps(track),))
            th.start()
            # redis_client.set()
    except ValueError as e:
        return render_template('error-api.html', user=current_user, message=str(e))
    # search_results = []
    # Render the search results
    return render_template('search.html', user=current_user, search_results=search_results)

@login_required
@views.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    # Get the song from the database
    song_id = request.form['song_id']
    if not song_id:
        flash('No song provided', category='error')
        redirect(url_for('views.library'))

    add_if_doesnt_exist(song_id)

    from website.models import Song, UserSongs
    song = Song.query.get(song_id)

    user_song = UserSongs.query.filter_by(user_id=current_user.id, song_id=song.id).first()

    if user_song:
        flash('Song is already in your playlist.', 'error')
    else:
        user_song = UserSongs(user_id=current_user.id, song_id=song.id)
        db.session.add(user_song)
        db.session.commit()
        flash('Song added to playlist.', 'success')
    return redirect(url_for('views.library'))

@views.route('/mark_as_listened', methods=['POST'])
@login_required
def mark_as_listened():
    from website.models import Song, UserSongs
    song_id = request.form.get('song_id')
    song = Song.query.get(song_id)
    user_song = UserSongs.query.filter_by(user_id=current_user.id, song_id=song.id).first()

    if not user_song:
        # The song is not in the user's playlist
        flash('Song is not in your playlist.')
        return redirect(url_for('home'))

    # Mark the song as listened
    user_song.listened = not user_song.listened
    db.session.commit()
    return redirect(url_for('views.library'))

@views.route('/remove_from_playlist', methods=['POST'])
def remove_from_playlist():
    from website.models import Song, UserSongs
    song_id = request.form.get('song_id')
    song = Song.query.get(song_id)
    user_song = UserSongs.query.filter_by(user_id=current_user.id, song_id=song.id).first()

    if not user_song:
        # The song is not in the user's playlist
        flash('Song is not in your playlist.')
        return redirect(url_for('home'))

    # Remove the song from the user's playlist
    db.session.delete(user_song)
    db.session.commit()
    return redirect(url_for('views.library'))


@views.route('/library/<string:short_id>')
def user_library(short_id):
    from website.models import User, UserSongs, Song
    user = User.query.filter_by(short_id=short_id).first()
    if user:
        if current_user.is_authenticated and current_user.id == user.id:
            return redirect(url_for('views.library'))
        user_songs = db.session.query(Song).join(UserSongs, UserSongs.song_id == Song.id).filter(UserSongs.user_id == user.id).all()
        return render_template('user_playlist.html', user=current_user, inspected_user=user, songs=user_songs)
    else:
        flash("Playlist not found", "error")
        return redirect(url_for('views.playlists'))

@views.route('/playlists')
def playlists():
    from website.models import User
    users = User.query.all()
    return render_template('all_playlists.html', user=current_user, users=users)
