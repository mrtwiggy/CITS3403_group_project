import unittest
from my_app import create_app, db
from my_app.models import User
from my_app.models import Franchise, Location, FranchiseLocation, Review

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testkey'

class ReviewCreationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.user = User(username="reviewer", email="reviewer@example.com")
        self.user.set_password("password")
        db.session.add(self.user)

        self.franchise = Franchise(name="Chatime")
        self.location = Location(name="Gongcha")
        db.session.add_all([self.franchise, self.location])
        db.session.commit()

        self.fr_loc = FranchiseLocation(franchise_id=self.franchise.id, location_id=self.location.id)
        db.session.add(self.fr_loc)
        db.session.commit()

    def login(self):
        return self.client.post('/auth/login', data={
            'email': self.user.email,
            'password': 'password'
        }, follow_redirects=True)

    def test_create_review(self):
        self.login()

        response = self.client.post('/review/create_review', data={
            'franchise_id': self.franchise.id,
            'location_id': self.location.id + self.franchise.id * 100,  # Encoding logic
            'drink_name': 'Matcha Milk Tea',
            'drink_size': 'M',
            'sugar_level': '50',
            'ice_level': '50',
            'review_content': 'Great drink!',
            'rating': '4',
            'is_private': '0',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        review = Review.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.drink_name, 'Matcha Milk Tea')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()