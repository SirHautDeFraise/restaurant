from flask import Flask
from markupsafe import escape
from flask import request
from flask import render_template
import sqlite3
import os
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
def hello_world():
    return 'yo'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/connexion')
def login():
    return "<p>login</p>"


@app.route('/disponibilites')
def reservation():
    tables = get_tables()
    return render_template('tablesList.html', tables=tables)


@app.route('/reservation/<int:reservation_id>/<string:reservation_periode>', methods=['GET', 'POST'])
def show_booking_table(reservation_id, reservation_periode):
    seats = get_seats(reservation_id, reservation_periode)
    return render_template('booking.html', reservation_id=reservation_id, reservation_periode=reservation_periode,
                           seats=seats)


@app.route('/annulerReservation/<int:reservation_id>/<string:reservation_periode>', methods=['GET'])
def cancel_booking(reservation_id, reservation_periode):
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
    data = request.form
    db = get_db()
    db.set_trace_callback(print)
    db.execute(
        "UPDATE tables SET status = 'Occupé' WHERE id= ? AND periode = ?",
        (data['reservation_id'], data['reservation_periode'],))
    db.commit()
    return render_template('bookingSuccess.html')
