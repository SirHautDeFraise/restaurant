from flask import Flask, session, url_for, flash
from markupsafe import escape
from flask import request
from flask import render_template
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


def is_not_logged():
    return session.get('id') is None


@app.route("/")
def home():
    if is_not_logged():
        return redirect(url_for('login'))
    return redirect(url_for('disponibilites'))


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/deconnexion')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/connexion', methods=('GET', 'POST'))
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


@app.route('/inscription', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        mail = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        if db.execute(
                'SELECT * FROM users WHERE mail = ?', (mail,)
        ).fetchone() is not None:
            error = "L'e-mail {} est déjà inscrit.".format(mail)

        if error is None:
            db.execute(
                'INSERT INTO users (firstname, lastname, mail, password)'
                + 'VALUES (?, ?, ?, ?)',
                (lastname, firstname, mail, password),
            )
            db.commit()
            return redirect(url_for('login'))

        flash(error)

    return render_template('register.html')


@app.route('/disponibilites')
def reservation():
    if is_not_logged():
        return redirect(url_for('login'))
    tables = get_tables()
    return render_template('tablesList.html', tables=tables)


@app.route('/reservation/<int:reservation_id>/<string:reservation_periode>', methods=['GET', 'POST'])
def show_booking_table(reservation_id, reservation_periode):
    if is_not_logged():
        return redirect(url_for('login'))
    seats = get_seats(reservation_id, reservation_periode)
    return render_template('booking.html', reservation_id=reservation_id, reservation_periode=reservation_periode,
                           seats=seats)


@app.route('/annulerReservation/<int:reservation_id>/<string:reservation_periode>', methods=['GET'])
def cancel_booking(reservation_id, reservation_periode):
    if is_not_logged():
        return redirect(url_for('login'))
    db = get_db()
    db.execute(
        "UPDATE tables SET status = 'Libre' WHERE id= ? AND periode = ?",
        (reservation_id, reservation_periode))
    db.commit()
    return render_template('cancelBookingSuccess.html')


# Return all tables in a dictionary as id => state
def get_tables():
    db = get_db()
    tables = db.execute(
        'SELECT * FROM tables'
    ).fetchall()
    return tables


def get_seats(table_id, periode):
    db = get_db()
    seats_number = db.execute(
        'SELECT seats FROM tables WHERE id = ? AND periode = ?', (table_id, periode,)
    ).fetchone()

    seats = []
    count = 1

    while count <= seats_number[0]:
        seats.append(count)
        count = count + 1
    return seats


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if is_not_logged():
        return redirect(url_for('login'))
    data = request.form
    db = get_db()
    db.set_trace_callback(print)
    db.execute(
        "UPDATE tables SET status = 'Occupé' WHERE id= ? AND periode = ?",
        (data['reservation_id'], data['reservation_periode'],))
    db.commit()
    return render_template('bookingSuccess.html')
