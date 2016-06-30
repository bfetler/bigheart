import os
import bigh
import unittest
import tempfile

class BighTestCase(unittest.TestCase):

    def setUp(self):
        bigh.app.config['TESTING'] = True
        bigh.app.config['DBNAME'] = 'bigh_test'   # must be created first
        self.app = bigh.app.test_client()
        with bigh.app.app_context():
            bigh.init_db()
        self.db_fd, self.data_path = tempfile.mkstemp()

    def tearDown(self):
        os.unlink(self.data_path)
        with bigh.app.app_context():
            bigh.init_db()

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

    def test_no_patients(self):
        self.login('admin', 'a-sharp')
        rv = self.app.get('/patients', follow_redirects=True)
        self.assertIn(b'Big Heart', rv.data)
        self.assertIn(b'No patients', rv.data)

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

    def test_add_no_xray_patient(self):
        self.login('admin', 'a-sharp')
        pat_id = 'abcd34'
        rv = self.app.post('/add', data=dict(patient_id=pat_id,
            gender='male', xray='False', double_density='True',
            oblique_diameter=5.4, appendage_shape='Convex'
        ), follow_redirects=True)
        self.assertIn(b'Big Heart', rv.data)
        self.assertIn(b'No Xray data', rv.data)

    def test_no_patient_info(self):
        self.login('admin', 'a-sharp')
        rv = self.app.post('/add', data=dict(
            title='BigHeart',
            text='HTML allowed here'
        ), follow_redirects=True)
        self.assertIn(u'Big Heart', rv.data)
        self.assertIn(u'Patient info incomplete', rv.data)

if __name__ == '__main__':
    unittest.main()

