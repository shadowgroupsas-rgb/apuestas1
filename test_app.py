import unittest
from app import app, db, User
from models import Settings
import os

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_sports_ai.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            user = User(username='admin', is_admin=True)
            user.set_password('admin123')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        if os.path.exists('test_sports_ai.db'):
            os.remove('test_sports_ai.db')

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.post('/login', data=dict(
            username='admin',
            password='admin123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_dashboard_access(self):
        # Login first
        self.app.post('/login', data=dict(
            username='admin',
            password='admin123'
        ), follow_redirects=True)

        # Access root, should redirect to dashboard
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

if __name__ == "__main__":
    unittest.main()
