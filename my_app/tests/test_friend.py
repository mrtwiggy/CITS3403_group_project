import unittest
from my_app import create_app, db
from my_app.models import User, Friendship

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testkey'

class FriendRequestTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create two users
        self.user1 = User(username="user1", email="user1@example.com")
        self.user2 = User(username="user2", email="user2@example.com")
        self.user1.set_password("password")
        self.user2.set_password("password")
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

    def login(self, user):
        with self.client:
            return self.client.post('/auth/login', data={
                'email': user.email,
                'password': 'password'
            }, follow_redirects=True)

    def test_send_friend_request(self):
        self.login(self.user1)
        response = self.client.post(f'/friends/request/{self.user2.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        friendship = Friendship.query.filter_by(user1_id=self.user1.id, user2_id=self.user2.id).first()
        self.assertIsNotNone(friendship)
        self.assertEqual(friendship.status, 'pending')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()