from flask import Flask, render_template
from redis.client import Redis

app = Flask(__name__)
redis_client = Redis(host="172.17.0.3", db=0, socket_connect_timeout=2, socket_timeout=2)

HOST = '0.0.0.0'
# redis_db = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def create_app():
    app.config['SECRET_KEY'] = "zaq1@WSXE62137xD"

    from .views import views
    app.register_blueprint(views, url_prefix='/')


    return app

