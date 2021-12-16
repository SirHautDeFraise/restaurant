import sqlite3
from flask import g
from flask import Flask
from markupsafe import escape
from flask import request
from flask import render_template
import os

DATABASE = 'bdd.db'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def query_add(query, args=()):
    cur = get_db().execute(query, args)
    cur.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if os.path.isfile('bdd.db') == False:
        with app.app_context():
            db = get_db()
            with app.open_resource('bdd.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

init_db()

@app.route('/')
def index():
    add = query_add("""insert into users(firstname,lastname) values(?,?)""",('olivier', 'giroud'))
    print(add)
    user = query_db('select * from users where id = ?',
                ['0'], one=True)
    if user is None:
        print('No such user')
    else:
       print(user['firstname'])
    return render_template('GFG.html',nom=('ouai'))





#@app.route("/")
#def hello_world():
#    return "<p>Hello</p>"


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
