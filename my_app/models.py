from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from my_app import db

# User Table
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username (must be unique)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email is now required
    password_hash = db.Column(db.String(128))  # Hashed password
    created_at = db.Column(db.DateTime, default=datetime.now)
    logged_in_at  = db.Column(db.DateTime,   nullable=True)
    profile_pic  = db.Column(db.String(255),nullable=True, default='pfp1.png')

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

    #data from other tables
    user_id= db.Column(db.Integer,db.ForeignKey('users.id', name='fk_reviews_users_id'),nullable=False)
    franchise_id = db.Column(db.Integer,db.ForeignKey('franchises.id', name='fk_reviews_franchises_id'),nullable=True)
    location_id = db.Column(db.Integer,db.ForeignKey('locations.id', name='fk_reviews_locations_id'), nullable=True)
    
    #data from reviews
    drink_name = db.Column(db.Text, nullable = False)
    drink_size = db.Column(db.String(20), nullable = False)
    review_content = db.Column(db.Text,nullable=False)
    
    sugar_level = db.Column(db.String(20),nullable=False)   # e.g. “25%”, “50%”
    ice_level = db.Column(db.String(20),nullable=False)   # e.g. “25%”, “50%”
    review_rating = db.Column(db.Integer,nullable=False)  # e.g. 1–5
    uploaded_at = db.Column(db.DateTime,nullable=False, default=datetime.now)

    # relationships
    user = db.relationship('User',back_populates='reviews')
    franchise = db.relationship('Franchise', backref='reviews',  lazy='joined')
    location = db.relationship('Location',  backref='reviews',  lazy='joined')

    def __repr__(self):
        return f"<Review {self.id} by User {self.user_id}>"

# Franchises table
class Franchise(db.Model):
    __tablename__ = 'franchises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    locations = db.relationship('Location', secondary='franchise_location', backref='franchises')

# Locations table
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Drinks table
class Drink(db.Model):
    __tablename__ = 'drinks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    locations = db.relationship('Franchise', secondary='franchise_drink', backref='drinks')

# Junction table for Franchises and Drinks (many-to-many)
class FranchiseDrink(db.Model):
    __tablename__ = 'franchise_drink'

    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', name='fk_franchisedrinks_drink_id'), primary_key=True)
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchises.id', name='fk_franchisedrinks_franchises_id'), primary_key=True)


# Junction table for Franchises and Locations (many-to-many)
class FranchiseLocation(db.Model):
    __tablename__ = 'franchise_location'
    
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchises.id', name='fk_franchiselocations_franchise_id'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', name='fk_franchiselocations_locations_id'), primary_key=True)