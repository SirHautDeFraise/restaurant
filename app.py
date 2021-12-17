from flask import Flask
from markupsafe import escape
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os

from werkzeug.utils import redirect
import db
from db import get_db

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'restaurant.sqlite'),
)
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


@app.route("/")
def base():
    return render_template('login.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        mail = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE mail = ?', (mail,)
        ).fetchone()

        # print(user)

        if user is None:
            error = 'Mauvais E-Mail.'
        elif user['password'] != password:
            error = 'Mauvais mot de passe.'

        if error is None:
            session.clear()
            session['id'] = user['id']
            session['firstname'] = user['firstname']
            session['lastname'] = user['lastname']
            session['email'] = user['mail']
            session['password'] = user['password']
            return redirect(url_for('register'))

        flash(error)

    return render_template('login.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        mail = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        # if error is None:
        #     try:
        #         db.execute(
        #             "INSERT INTO users (firstname, lastname, mail, password) VALUES (?, ?, ?, ?)",
        #             (lastname, firstname, mail, password),
        #             )
            
        #         db.commit()
        #     except db.IntegrityError:
        #         error = f"User {mail} is already registered."
        #     else:
        #         return redirect(url_for("auth.login"))
        if db.execute(
            'SELECT * FROM users WHERE mail = ?', (mail,)
        ).fetchone() is not None:
            error = 'Cet E-Mail {} est déjà inscrit.'.format(mail)

        if error is None:
            db.execute(
                'INSERT INTO users (firstname, lastname, mail, password)'
                + 'VALUES (?, ?, ?, ?)',
                (lastname, firstname, mail,password),
                )
            db.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('register.html')