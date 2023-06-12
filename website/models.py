from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class UserSongs(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    listened = db.Column(db.Boolean, default=False)
    song = db.relationship("Song", back_populates="users")
    user = db.relationship("User", back_populates="songs")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    songs = db.relationship('UserSongs', back_populates='user')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('UserSongs', back_populates='song')



