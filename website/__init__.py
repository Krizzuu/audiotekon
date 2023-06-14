from flask import Flask
from flask_login import LoginManager
from munch import DefaultMunch
from flask_sqlalchemy import SQLAlchemy

from website.redis_wrapper import RedisWrapper

app = Flask(__name__)
db = SQLAlchemy()
redis_client = RedisWrapper()

def add_if_doesnt_exist(song_id):
    from website.models import Song
    import json
    song = Song.query.get(song_id)
    if song:
        return
    song_data = redis_client.get(song_id)
    if not song_data:
        from website.api_service.api_utils import get_track
        song_data = get_track(song_id)
    else:
        song_data = json.loads(song_data)
        song_data = DefaultMunch.fromDict(song_data)

    if not song:
        new_song = Song(id=song_data.commontrack_id, artist=song_data.artist_name, name=song_data.track_name)
        db.session.add(new_song)
        db.session.commit()

def create_app():
    app.config['SECRET_KEY'] = "zaq1@WSXE62137xD"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@db/audiotekon_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
