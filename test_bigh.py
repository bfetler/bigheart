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
        self.assertIn(b'Big Heart', rv.data)
        self.assertIn(b'log in', rv.data)
#       assert b'log in' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'a-sharp')
        self.assertIn(b'You were logged in', rv.data)
        self.assertIn(b'Patient ID', rv.data)
        self.assertIn(b'Xray', rv.data)
        rv = self.logout()
        self.assertIn(b'You were logged out', rv.data)
        rv = self.login('adminx', 'a-sharp')
        self.assertIn(b'Invalid username', rv.data)
        rv = self.login('admin', 'defaultx')
        self.assertIn(b'Invalid password', rv.data)

#   def test_no_patients(self):
#       self.login('admin', 'a-sharp')
#       rv = self.app.get('/patients', follow_redirects=True)
#       self.assertIn(b'Big Heart', rv.data)
# next line fails if patients, using same db as app for now
#       self.assertIn(b'No patients', rv.data)

    def test_new_patient(self):
        self.login('admin', 'a-sharp')
        rv = self.app.get('/new', follow_redirects=True)
        self.assertIn(b'Big Heart', rv.data)
        self.assertIn(b'Patient List', rv.data)
        self.assertIn(b'Patient ID', rv.data)
        self.assertIn(b'Xray', rv.data)

# could test a variety of input, find different outcomes in html
    def test_add_severe_patient(self):
        self.login('admin', 'a-sharp')
        pat_id = 'abcd12'
        rv = self.app.post('/add', data=dict(patient_id=pat_id,
            gender='male', xray='True', double_density='True',
            oblique_diameter=5.4, appendage_shape='Convex'
        ), follow_redirects=True)
        self.assertIn(b'Big Heart', rv.data)
        self.assertIn(b'New patient was successfully posted', rv.data)
        self.assertIn(b'Severe', rv.data)
        self.assertIn(b'Date &amp; Time', rv.data)
        bigh.remove_one_patient(pat_id)  # clean up db after

    def grr_show_patient(self):
        self.login('admin', 'a-sharp')
# one way to add it in db?
# use self.db_fd ?
        self.app.post('/add', data=dict(patient_id='abcd12',
            gender='male', xray='True', double_density='True',
            oblique_diameter=5.4, appendage_shape='Convex'
        ), follow_redirects=True)
        rv = self.app.get('/patients/abcd12', follow_redirects=True)
        self.assertIn(u'Big Heart', rv.data)
        self.assertIn(u'Severe', rv.data)

    def grr_messages(self):    # for flaskr, irrelevant fields in data
        self.login('admin', 'a-sharp')
        rv = self.app.post('/add', data=dict(
            title='<BigHeart>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
#       self.assertIn(u'Big Heart', rv.data)
#       self.assertNotIn(u'No patients', rv.data)
#       self.assertIn(u'&lt;BigHeart&gt;', rv.data)
#       self.assertIn(u'<strong>HTML</strong> allowed here', rv.data)

    def test_req_context(self):   # works but is it useful?
        app = bigh.Flask('bigh')
        with app.test_request_context('/?name=Peter'):
            self.assertEqual(bigh.request.path, '/')
            self.assertEqual(bigh.request.args['name'], 'Peter')

if __name__ == '__main__':
    unittest.main()


