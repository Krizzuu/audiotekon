from flask import Flask, render_template
from flask_login import LoginManager
from redis.client import Redis
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
redis_client = Redis(host="redis", port=6379, db=0, socket_connect_timeout=2, socket_timeout=2, decode_responses=True)

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
