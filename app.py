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
        mdp = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE mail = ?', (mail,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['mdp'], mdp):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html', mail=mail, mdp=mdp, db=db)

    # if request.form['email'] != 'thibou@gmail.com' or request.form['password'] != 'mdp':
    #     error = 'Mauvais E-mail/Mot de passe.'
    # else:
    #     return redirect(url_for('reservation'))
    # return render_template('login.html', error=error)

    # email = request.form['email']
    # pwd = request.form['password']
    # if email not in database:
    #     return render_template('login.html')
    # else:
    #     if database[email] != pwd:
    #         return render_template('login.html')
    #     else:
    #         return render_template('base.html', name=email)


@app.route('/inscription', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


# @app.route('/disponibilites')
# def reservation():
#     tables = get_tables()
#     return render_template('tablesList.html', tables=tables)


# @app.route('/reservation')
# def show_booking():
#     free_tables = get_free_tables()
#     return render_template('booking.html', free_tables=free_tables)


# @app.route('/reservation/<int:reservation_id>', methods=['GET', 'POST'])
# def show_booking_table(reservation_id):
#     return render_template('booking.html', reservation_id=reservation_id)

# Return all tables in a dictionary as id => state


# def get_tables():
#     db = get_db()
#     tables = db.execute(
#         'SELECT * FROM tables'
#     ).fetchall()
#     return tables

# Return all tables that are free


# def get_free_tables():
#     tables = get_tables()
#     free_tables = []
#     for table in tables:
#         for table_id, status in table.items():
#             if status == "libre":
#                 free_tables.append(table_id)
#     return free_tables
