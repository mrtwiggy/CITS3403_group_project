# my_app/routes/main.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from my_app.forms import ReviewForm
from my_app import db 

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/update_profile_pic', methods=['POST'])
@login_required
def update_profile_pic():
    selected_pic = request.form.get('profile_pic')
    current_user.profile_pic = selected_pic
    db.session.commit()
    flash('Profile picture updated!', 'success')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/recent_reviews')
def recent_reviews():
    return render_template('recent_reviews.html')

@main_bp.route('/explore')
def explore():
    return render_template('explore.html')