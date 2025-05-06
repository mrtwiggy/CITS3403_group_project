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
