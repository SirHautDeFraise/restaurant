from flask import Flask
from markupsafe import escape
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route("/")
def base():
    return render_template('base.html')


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/connexion')
def login():
    return "<p>login</p>"


@app.route('/inscription', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
