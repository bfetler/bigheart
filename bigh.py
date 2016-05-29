# big heart - a flask demo project

# all the imports
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.exceptions import BadRequestKeyError

from contextlib import closing  # for database init
from formulas import getXrayOutcome
from helpers import getDateStr, getNowTimeInt, int2bool, bool2int, \
     int2choice, choice2int, appendage2choice, choice2appendage, \
     get_menu, gender_choices, gender_menu_choices, get_gender_menu

# configuration - put in env instead of file?
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

# not used?
def get_params(patient_id):
    '''Query database for single patient row.'''
    rv = query_db('select gender from patients where patient_id = ?',
        [patient_id], one=True)
    return rv[0] if rv else None


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
    cur = g.db.execute('select patient_id, date_created, xray_outcome from patients order by id desc')
    patients = [dict(patient_id=row[0], datetime=getDateStr(row[1]), xray_outcome=row[2]) for row in cur.fetchall()]
    return render_template('show_patients.html', patients=patients)

# let user add new patient if logged in
#    responds to POST not GET, actual form is in show_patients.html
#    logged_in key is present and True
#    use ? in SQL to avoid SQL injection
@app.route('/add', methods=['POST'])
def add_patient():
    if not session.get('logged_in'):
        abort(401)
    patient_id = request.form['patient_id']
    dz = getNowTimeInt()
    gender = request.form['gender']
    xray = bool2int(request.form['xray'])
    ddensity = choice2int(request.form['double_density'])
    ob_diam = float(request.form['oblique_diameter'])  # check < 0.0
    app_shape = choice2appendage(request.form['appendage_shape'])
#   g = request.form['gender']   # cannot request.form same object twice
#   g, x = request.form['gender'], request.form['xray']
#   redirect if not all params reasonable? restrict on form is not enough?
#   (param validation)
    x_outcome = ''
    if (xray > 0):
        x_outcome = getXrayOutcome(gender, ddensity, ob_diam, app_shape)
    ctmri = 0
# should be ok with postgres too --dillon
    g.db.execute('insert into patients (patient_id, gender, date_created, \
                  xray, double_density, oblique_diameter, \
                  appendage_shape, xray_outcome, ctmri) values \
                  (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 [patient_id, gender, dz, xray, ddensity, ob_diam,
                  app_shape, x_outcome, ctmri])
    g.db.commit()
    app.logger.warning('debug: add_patient: patient_id=%s app_shape=%d xray_outcome=%s', patient_id,  app_shape, x_outcome)
    gen3 = "gen3"
    try:
        gen3 = request.form['gender3']
        app.logger.warning('gender_menu type %s', type(gen3))
        if (gen3):
            app.logger.warning('gender_menu=%s', gen3)
    except (BadRequestKeyError, Exception) as inst:
        app.logger.warning('request.form %s', str(type(request.form)))
        app.logger.warning('request.form gender3 not found')
        app.logger.warning("inst type %s args %s inst %s", str(type(inst)), inst.args, inst)
#       raise
#       raise BadRequestKeyError(*inst.args)
        flash('Patient info incomplete, please re-enter')
        return redirect(url_for('new_patient', patient_id=patient_id))
# would be nice to redirect back to previous page w/ info entered
    flash('New patient was successfully posted')
    return redirect(url_for('show_patient', patient_id=patient_id))
# what can I do with this?
#    redirect if form incomplete (not store in db)
#    re-raise exception
#    log messages

@app.route('/')
@app.route('/new/')
def new_patient():
    return render_template(
        'show_patient.html', patient=None,
#       gender_menu=gender_menu_choices()
#       gender_menu=get_menu('gender', gender_choices())
        gender_menu = get_gender_menu()
    )

@app.route('/patient/<patient_id>')
def show_patient(patient_id):
#   print 'show_patient id', patient_id
#   cur = g.db.execute('select gender from patients where patient_id = ? order by id desc', patient_id)
#   patient = [dict(pid=row[0], gender=row[1]) for row in cur.fetchall()]
#   patient = get_params(patient_id)  # works for one param
    rq = query_db('select date_created, gender, xray, double_density, \
         oblique_diameter, appendage_shape, xray_outcome, ctmri from patients where \
         patient_id = ?',
        [patient_id], one=True)
    patient = None
    if rq:
        ddate    = getDateStr(rq[0])
        gender   = rq[1]
        xray     = int2bool(rq[2])
        ddensity = int2choice(rq[3])
        oblique_diam = float(rq[4])
        app_shape = appendage2choice(rq[5])
        xray_outcome = rq[6]
        ctmri    = int2bool(rq[7])
        patient  = dict(patient_id=patient_id, datetime=ddate, gender=gender, 
            xray=xray, double_density=ddensity, oblique_diameter=oblique_diam,
            appendage_shape=app_shape,
            xray_outcome=xray_outcome, ctmri=ctmri)
#   print 'show_patient', patient
    app.logger.warning('debug: show_patient: pid=%s xray=%s app_shape=%s x_outcome=%s', patient['patient_id'], patient['xray'], patient['appendage_shape'], patient['xray_outcome'])
#   app.logger.warning('debug: show_patient: pid=%s id=%d gender=%s', patient['patient_id'], patient['id'], patient['gender'])  # works, tuple index is int
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
            return redirect(url_for('new_patient'))
    return render_template('login.html', error=error)

# user logout
#    pop w/ 2nd param deletes key if present, do nothing if not present
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect('/')


# allows you to start this file as a server, as a standalone application
if __name__ == '__main__':
    app.run()

# run it with:
# python bigheart.py
#   *  Running on http://127.0.0.1:5000/

