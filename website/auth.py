from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # if user:
        #     if check_password_hash(user.password, password):
        #         flash('Logged in successfully!', category='success')
        #         login_user(user, remember=True)
        #         return redirect(url_for('views.home'))
        #     else:
        #         flash('Incorrect password, try again.', category='error')
        # else:
        #     flash('Email does not exist.', category='error')

    return render_template("login.html")