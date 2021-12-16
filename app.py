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


@app.route('/reservation')
def show_booking():
    free_tables = get_free_tables()
    return render_template('booking.html', free_tables=free_tables)


@app.route('/reservation/<int:reservation_id>', methods=['GET', 'POST'])
def show_booking_table(reservation_id):
    return render_template('booking.html', reservation_id=reservation_id)


# Return all tables in a dictionary as id => state
def get_tables():
    db = get_db()
    tables = db.execute(
        'SELECT * FROM tables'
    ).fetchall()
    return tables

# Return all tables that are free
def get_free_tables():
    tables = get_tables()
    free_tables = []
    for table in tables:
        for table_id, status in table.items():
            if status == "libre":
                free_tables.append(table_id)
    return free_tables