import os
import bigh
import unittest
import tempfile

class BighTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, bigh.app.config['DATABASE'] = tempfile.mkstemp()
        bigh.app.config['TESTING'] = True
        self.app = bigh.app.test_client()
        bigh.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(bigh.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Big Heart' in rv.data
        assert 'log in' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'a-sharp')
        assert 'You were logged in' in rv.data
        assert 'Patient ID' in rv.data
        assert 'Xray' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'a-sharp')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_no_patients(self):
        self.login('admin', 'a-sharp')
        rv = self.app.get('/patients', follow_redirects=True)
        assert 'Big Heart' in rv.data
        assert 'No patients' in rv.data

    def test_new_patient(self):
        self.login('admin', 'a-sharp')
        rv = self.app.get('/new', follow_redirects=True)
        assert 'Big Heart' in rv.data
        assert 'Patient List' in rv.data
        assert 'Patient ID' in rv.data
        assert 'Xray' in rv.data

# could test a variety of input, find different outcomes in html
    def test_add_severe_patient(self):
        self.login('admin', 'a-sharp')
        rv = self.app.post('/add', data=dict(patient_id='abcd12',
            gender='male', xray='True', double_density='True',
            oblique_diameter=5.4, appendage_shape='Convex'
        ), follow_redirects=True)
        assert 'Big Heart' in rv.data
        assert 'New patient was successfully posted' in rv.data
        assert 'Severe' in rv.data
        assert 'Date &amp; Time' in rv.data

    def grr_show_patient(self):
        self.login('admin', 'a-sharp')
# one way to add it in db?
# use self.db_fd ?
        self.app.post('/add', data=dict(patient_id='abcd12',
            gender='male', xray='True', double_density='True',
            oblique_diameter=5.4, appendage_shape='Convex'
        ), follow_redirects=True)
        rv = self.app.get('/patients/abcd12', follow_redirects=True)
        assert 'Big Heart' in rv.data
        assert 'Severe' in rv.data

    def grr_messages(self):    # for flaskr, irrelevant fields in data
        self.login('admin', 'a-sharp')
        rv = self.app.post('/add', data=dict(
            title='<BigHeart>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
#       assert 'Big Heart' in rv.data
#       assert 'No patients' not in rv.data
#       assert '&lt;BigHeart&gt;' in rv.data
#       assert '<strong>HTML</strong> allowed here' in rv.data

    def test_req_context(self):   # works but is it useful?
        app = bigh.Flask('bigh')
        with app.test_request_context('/?name=Peter'):
            assert bigh.request.path == '/'
            assert bigh.request.args['name'] == 'Peter'

if __name__ == '__main__':
    unittest.main()


