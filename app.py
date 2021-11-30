from flask import Flask
from markupsafe import escape
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello</p>"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/connexion')
def login():
    return "<p>login</p>"


@app.route('/reservation')
def hello(name=None):
    return render_template('hello.html', name=name)
