# big heart - a flask demo project

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from contextlib import closing  # for database init

import datetime
import time

# configuration
DATABASE = '/tmp/bigh2.db'
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
#    sqlite3 /tmp/bigh2.db < schema.sql
#    substitute in the DATABASE path above

# datetime methods:
# import datetime
# import time     # dz - seconds since 1/1/1970
# dz = int(time.mktime(datetime.datetime.now().timetuple()))
# dd = datetime.datetime.fromtimestamp(dz)

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

# one=True, return just 1st item in query
def query_db(query, args=(), one=False):
    '''Query database and return list of dictionaries.'''
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

# actually I want to get multiple fields from db for given id
def get_params(patient_id):
    rv = query_db('select sex from patients where patient_id = ?',
        [patient_id], one=True)
    return rv[0] if rv else None

# helper method, should use boolean not string
def int2bool(intval):
    return 'False' if intval == 0 else 'True'

def bool2int(str):
    return 1 if str == 'True' else 0

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
# @app.route('/')
@app.route('/patients/')
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
    dz = int(time.mktime(datetime.datetime.now().timetuple()))  # since 1970
    g.db.execute('insert into patients (patient_id, sex, date_created, \
                  xray, ct_mri) values (?, ?, ?, ?, ?)',
                 [request.form['patient_id'], request.form['sex'], dz, 
                  bool2int(request.form['xray']), 0])
    g.db.commit()
    flash('New patient was successfully posted')
    return redirect(url_for('show_patients'))

@app.route('/')
@app.route('/new/')
def new_patient():
    return render_template('show_patient.html', patient=None)

@app.route('/patient/<patient_id>')
def show_patient(patient_id):
    print 'show_patient id', patient_id
#   cur = g.db.execute('select sex from patients where patient_id = ? order by id desc', patient_id)
#   patient = [dict(pid=row[0], sex=row[1]) for row in cur.fetchall()]
#   patient = get_params(patient_id)  # works for one param
    rq = query_db('select sex, id, date_created, xray, ct_mri from patients where patient_id = ?',
        [patient_id], one=True)
    patient = None
    if rq:
        dd = datetime.datetime.fromtimestamp(rq[2])
        dd = str(dd.strptime(str(dd), "%Y-%m-%d %H:%M:%S"))
        xray   = int2bool(rq[3])
        ct_mri = int2bool(rq[4])
        patient = dict(sex=rq[0], id=rq[1], datetime=dd, xray=xray,
            ct_mri=ct_mri, patient_id=patient_id)
#       patient['patient_id'] = patient_id
    print 'show_patient', patient
#   app.logger.warning('debug: show_patient: pid=%s id=%d sex=%s', patient['patient_id'], patient['id'], patient['sex'])  # works, tuple index is int
#   abort(401)
    return render_template('show_patient.html', patient=patient)

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
#           return redirect(url_for('show_patients'))
            return redirect(url_for('new_patient'))
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

