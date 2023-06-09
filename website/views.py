from flask import Blueprint, render_template, session, request, flash
from flask_login import login_required, current_user

from website import redis_client

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    import os
    api_key = os.getenv("API_KEY")
    return render_template("home.html", user=current_user)
