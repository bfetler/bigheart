# big heart - a flask demo project

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from contextlib import closing  # for database init

# configuration
DATABASE = '/tmp/bigh1.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'a-sharp'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# read config from ENV variable - skip for now
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# when first starting app, don't forget:
#    sqlite3 /tmp/flaskr.db < schema.sql

# connect to database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# init database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# now you can create a db in a python script:
# from flaskr import init_db
# init_db()

# decorators, run special functions before db request, 
# after db request @app.after_request \n def after_request():
# if db request throws exception (teardown)
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# start view controller section
#    view templates in templates/, they use Jinja2 w// autoescaping
#    views also use template inheritance, e.g. {% block body %}

# show all patients in db
@app.route('/')
def show_patients():
    cur = g.db.execute('select patient_id, sex from patients order by id desc')
    patients = [dict(patient_id=row[0], sex=row[1]) for row in cur.fetchall()]
    return render_template('show_patients.html', patients=patients)

# let user add new patient if logged in
#    responds to POST not GET, actual form is in show_patients.html
#    logged_in key is present and True
#    use ? in SQL to avoid SQL injection
@app.route('/add', methods=['POST'])
def add_patient():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into patients (patient_id, sex) values (?, ?)',
                 [request.form['patient_id'], request.form['sex']])
    g.db.commit()
    flash('New patient was successfully posted')
    return redirect(url_for('show_patients'))

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_patients'))
    return render_template('login.html', error=error)

# user logout
#    pop w/ 2nd param deletes key if present, do nothing if not present
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_patients'))


# allows you to start this file as a server, as a standalone application
if __name__ == '__main__':
    app.run()

# run it with:
# python bigheart.py
#   *  Running on http://127.0.0.1:5000/

