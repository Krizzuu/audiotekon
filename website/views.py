from flask import Blueprint, render_template, session

from website import redis_client

views = Blueprint('views', __name__)

@views.route("/")
def home():
    redis_client.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis_client.get('hits')

