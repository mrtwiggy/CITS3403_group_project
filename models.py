from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy (the database ORM)
db = SQLAlchemy()

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username (must be unique)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email is now required
    password_hash = db.Column(db.String(128))  # Hashed password
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login_at    = db.Column(db.DateTime,   nullable=True)
    profile_pic_url  = db.Column(db.String(255),nullable=True)

    reviews = db.relationship('Review', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}>"
    # Set the user's password (hashes it for security)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check if a password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Review(db.Model):
    __tablename__ = 'reviews'

    id= db.Column(db.Integer,primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    
    # If you’ve already got Franchises, Drinks and Locations tables,
    # link to them with real FKs; otherwise store names as plain strings:
    drink_id = db.Column(db.Integer,db.ForeignKey('drinks.id'),   nullable=True)
    franchise_id = db.Column(db.Integer,db.ForeignKey('franchises.id'),nullable=True)
    location_id = db.Column(db.Integer,db.ForeignKey('locations.id'), nullable=True)
    
    review_content = db.Column(db.Text,nullable=False)
    sugar_level = db.Column(db.String(20),nullable=True)   # e.g. “25%”, “Half”
    ice_level = db.Column(db.String(20),nullable=True)   # e.g. “No ice”, “Light ice”
    review_rating = db.Column(db.Integer,nullable=False)  # e.g. 1–5
    uploaded_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)

    # relationships
    user = db.relationship('User',back_populates='reviews')
    drink = db.relationship('Drink',backref='reviews',  lazy='joined')
    franchise = db.relationship('Franchise', backref='reviews',  lazy='joined')
    location = db.relationship('Location',  backref='reviews',  lazy='joined')

    def __repr__(self):
        return f"<Review {self.id} by User {self.user_id}>"
