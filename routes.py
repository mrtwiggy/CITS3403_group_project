from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, LoginForm, SignupForm
from models import User

#routes for signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        #checks if the username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
        
        #checks if the email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
            return redirect(url_for('signup'))
        
        #sets the user input into the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

#route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

#route for dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

#route to update profile pic
@app.route('/update_profile_pic', methods=['POST'])
@login_required
def update_profile_pic():
    selected_pic = request.form.get('profile_pic')
    current_user.profile_pic = selected_pic
    db.session.commit()
    flash('Profile picture updated!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/recent_reviews')
def recent_reviews():
    return render_template('recent_reviews.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')