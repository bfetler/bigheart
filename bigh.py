# big heart - a flask demo project
# python 2.7

# import sqlite3
import psycopg2
# import pdb       # pdb.set_trace()  # sets breakpoint

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug.exceptions import BadRequestKeyError

from contextlib import closing  # used in init_db()
from formulas import getXrayOutcome
from helpers import getDateStr, getNowTimeInt, int2bool, bool2int, \
     int2choice, choice2int, appendage2choice, choice2appendage, \
     get_gender_menu, get_ddensity_menu, get_appendage_menu

DATABASE = '/tmp/bigh2.db'   # sqlite3
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'a-sharp'

app = Flask(__name__)
app.config.from_object(__name__)

# read config from ENV variable - skip for now
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# when first starting app w/ sqlite3:
#    sqlite3 /tmp/bigh2.db < schema.sql
#    substitute in the DATABASE path above

def connect_db():
    "connect to database"
    try:
#       return sqlite3.connect(app.config['DATABASE'])
        return psycopg2.connect("dbname=flaskdb user=postgres host=localhost")
    except:
        print("cannot connect to db")
        raise

def init_db():
    "init database for sqlite3"
    with closing(connect_db()) as db:
        with app.open_resource('schema_lite.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    "Query database and return list of dictionaries, or just one item."
    cur = g.db.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_params(patient_id):
    '''Query database for single patient row.'''
    rv = query_db('select date_created from patients where patient_id = %s;',
        [patient_id], one=True)
    return rv[0] if rv else None


# decorators, run special functions before / after db request, 
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# start view controller section
#    view templates in templates/, using Jinja2 w/ autoescaping
#    views also use template inheritance, e.g. {% block body %}

@app.route('/patients/')
def show_patients():
    "show all patients in db"
    cur = g.db.cursor()
    cur.execute('SELECT patient_id, date_created, xray_outcome FROM patients ORDER BY id desc;')
    if cur:
        patients = [dict(patient_id=row[0], datetime=getDateStr(row[1]), xray_outcome=row[2]) for row in cur.fetchall()]
    else:
        patients = []
    return render_template('show_patients.html', patients=patients)

# respond to POST, form is show_patients.html
@app.route('/add', methods=['POST'])
def add_patient():
    "add new patient if logged in"
    if not session.get('logged_in'):  # logged_in key present and True
        abort(401)
    try:
        xray = bool2int(request.form['xray'])
        if not xray:
# special case: cannot make xray diagnosis, should not commit
            flash('No Xray data, cannot make diagnosis')
            return redirect(url_for('new_patient'))

        patient_id = request.form['patient_id']   # should not be empty
        if len(patient_id) < 5:
# could flash(msg)
            raise BadRequestKeyError('patient id invalid, too short')
        ddensity = choice2int(request.form['double_density'])
        ob_diam = float(request.form['oblique_diameter'])
        app_shape = choice2appendage(request.form['appendage_shape'])
        gender = request.form['gender']
    except (BadRequestKeyError, Exception) as inst:
        app.logger.warning('request.form %s', str(type(request.form)))
        app.logger.warning("inst type %s args %s inst %s", str(type(inst)), inst.args, inst)
#       raise
#       raise BadRequestKeyError(*inst.args)
        flash('Patient info incomplete, please re-enter')
        return redirect(url_for('new_patient'))
# what can I do with this?
#    redirect if form incomplete (not store in db)
#    re-raise exception
#    log messages

    has_patient = get_params(patient_id)
    app.logger.warning('patient_id %s exists %s', patient_id, str(has_patient))
    if has_patient:
        flash("patient id '%s' already exists, please re-enter" % patient_id)
        return redirect(url_for('new_patient'))

    x_outcome = ''
    if (xray > 0):
        x_outcome = getXrayOutcome(gender, ddensity, ob_diam, app_shape)
    dz = getNowTimeInt()
    ctmri = 0
    cur = g.db.cursor()
    cur.execute('insert into patients (patient_id, gender, date_created, \
                  xray, double_density, oblique_diameter, \
                  appendage_shape, xray_outcome, ctmri) values \
                  (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                 (patient_id, gender, dz, xray, ddensity, ob_diam,
                  app_shape, x_outcome, ctmri))
    g.db.commit()
    flash('New patient was successfully posted')
    return redirect(url_for('show_patient', patient_id=patient_id))

@app.route('/')
@app.route('/new/')
def new_patient():
    "show new patient form"
    return render_template(
        'show_patient.html', patient=None,
        gender_menu = get_gender_menu(),
        ddensity_menu = get_ddensity_menu(),
        appendage_shape_menu = get_appendage_menu()
    )

@app.route('/patient/<patient_id>')
def show_patient(patient_id):
    "show patient with given patient_id"
    rq = query_db('select date_created, gender, xray, double_density, \
         oblique_diameter, appendage_shape, xray_outcome, ctmri from patients \
         where patient_id = %s;',
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
    return render_template('show_patient.html', patient=patient)

@app.route('/login', methods=['GET', 'POST'])
def login():
    "user login"
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

#    pop w/ 2nd param deletes key if present, do nothing if not present
@app.route('/logout')
def logout():
    "user logout"
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect('/')


# lets you start this file as a server, standalone application
if __name__ == '__main__':
    app.run()

# run it with:
# python bigheart.py
#   *  Running on http://127.0.0.1:5000/

