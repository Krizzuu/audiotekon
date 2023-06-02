from flask import Blueprint, render_template, session, request, flash
from flask_login import login_required

from website import redis_client

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=None)
