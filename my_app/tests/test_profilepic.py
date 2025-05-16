import unittest
from my_app import create_app, db
from my_app.models import User

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testkey'

class UpdateProfilePicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.user = User(username="profileuser", email="pic@example.com")
        self.user.set_password("password")
        db.session.add(self.user)
        db.session.commit()

    def login(self):
        return self.client.post('/auth/login', data={
            'email': self.user.email,
            'password': 'password'
        }, follow_redirects=True)

    def test_update_profile_pic(self):
        self.login()

        response = self.client.post('/update_profile_pic', data={
            'profile_pic': 'pfp1.png'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        updated_user = User.query.get(self.user.id)
        self.assertEqual(updated_user.profile_pic, 'pfp1.png')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()
