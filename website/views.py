from flask import Blueprint, render_template, session

from website import redis_client

views = Blueprint('views', __name__)

@views.route("/")
def home():
    user = session.get('user')
    if not user:
        user = "Not logged in"

    redis_client.set("gege", "haha")

    return render_template("index.html", user=user)


@views.route("/test")
def test():
    return redis_client.get("gege")