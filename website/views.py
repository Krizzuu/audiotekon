from flask import Blueprint, render_template, session, request, flash
from flask_login import login_required

from website import redis_client

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')#Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            flash('Note added!', category='success')

    return render_template("home.html", user=None)
