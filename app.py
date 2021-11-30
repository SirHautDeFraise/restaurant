from flask import Flask
from markupsafe import escape
from flask import request
from flask import render_template
import sqlite3

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello World</p>"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/connexion')
def login():
    return "<p>login</p>"


@app.route('/reservation')
def reservation():
    tables = get_tables_id()
    return render_template('tablesList.html', tables=tables)


def get_tables_id():
    tables = [{1: "libre", 2: "occupé", 3: "libre", 4: "occupé", 5: "libre"}]
    return tables
