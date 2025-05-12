# my_app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from my_app import db
from my_app.models import User, Franchise  # Import from my_app.models, not just models
from my_app.forms import LoginForm, SignupForm
from datetime import datetime

# Create a blueprint
auth_bp = Blueprint('auth', __name__)

# Routes for signup
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # Checks if the username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.signup'))
        
        # Checks if the email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.signup'))
        
        # Sets the user input into the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form, hide_nav=True)

# Route for login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():      
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            current_user.logged_in_at = datetime.now()
            db.session.commit()
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form, hide_nav=True)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))