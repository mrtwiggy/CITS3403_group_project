from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy (the database ORM)
db = SQLAlchemy()

# User Table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # Username (must be unique)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email is now required
    password_hash = db.Column(db.String(128))  # Hashed password
    created_at = db.Column(db.DateTime, default=datetime.now)
    logged_in_at = db.Column(db.DateTime, nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True, default='profilepic1.png')

    # Set the user's password (hashes it for security)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check if a password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# Franchises table
class Franchise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    locations = db.relationship('Location', secondary='franchise_location', backref='franchises')

# Locations table
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Drinks table
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    locations = db.relationship('Location', secondary='location_drink', backref='drinks')

# Reviews table
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drink_name = db.Column(db.String(100), nullable=False)
    franchise = db.Column(db.String(100))
    location = db.Column(db.String(100))
    review_content = db.Column(db.Text)
    sugar_level = db.Column(db.String(50))
    ice_level = db.Column(db.String(50))
    toppings = db.Column(db.String(200))  # comma-separated toppings for now
    review_rating = db.Column(db.Integer)
    date_uploaded = db.Column(db.DateTime, default=datetime.now)

# Junction table for Drinks and Locations (many-to-many)
class LocationDrink(db.Model):
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)

# Junction table for Franchises and Locations (many-to-many)
class FranchiseLocation(db.Model):
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchise.id'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), primary_key=True)