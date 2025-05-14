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
    
    #get all friends for a user
    def get_all_friends(self):
        friendships = Friendship.query.filter(
            ((Friendship.user1_id == self.id) | (Friendship.user2_id == self.id)) &
            (Friendship.status == 'accepted')
        ).all()

        friends = []
        for f in friendships:
            if f.user1_id == self.id:
                friends.append(f.user2)
            else:
                friends.append(f.user1)
        return friends
    
    def has_friend_requests_pending(self):
        current_requests = Friendship.query.filter(
            ((Friendship.user2_id == self.id)) &
            (Friendship.status == 'pending')
        ).all()

        return bool(current_requests)
    
    #received friends of a user -> returns list of requests sent to user
    def received_friend_requests(self):
        current_requests = Friendship.query.filter(
            ((Friendship.user2_id == self.id)) &
            (Friendship.status == 'pending')
        ).all()

        requests= []
        for f in current_requests:
            if f.user1_id == self.id:
                requests.append(f.user2)
            else:
                requests.append(f.user1)
        return requests
    
    #returns boolean value of friendship existing
    def is_friend_with(self, user):
        friendship = Friendship.query.filter(
            ((Friendship.user1_id == self.id & Friendship.user2_id == user.id) | 
             (Friendship.user1_id == user.id & Friendship.user2_id == self.id)) &
            (Friendship.status == 'accepted')
        ).all()

        return bool(friendship)
    
    #changes 'pending' line in table to 'accept'
    def accept_friend_request(self, user):
        # Find the pending friendship request between user1 and user2
        pending_request = Friendship.query.filter(
            (Friendship.user1_id == user.id) &
            (Friendship.user2_id == self.id) &
            (Friendship.status == 'pending')
        ).first()  # Use .first() to get a single result

        if pending_request:
            # Update the status to 'accepted'
            pending_request.status = 'accepted'
            db.session.commit()  # Save the changes to the database
            return True  # Successfully accepted the request

        return False  # No pending request found

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

    #private/public
    is_private = db.Column(db.Boolean, default=False)

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

# Friendship model
class Friendship(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(100), nullable=False)

    user1 = db.relationship('User', foreign_keys=[user1_id], backref='friendships_sent')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='friendships_received')


