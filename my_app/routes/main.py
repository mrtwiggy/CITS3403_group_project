# my_app/routes/main.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from my_app.forms import ReviewForm
from my_app.models import Franchise, Review
from sqlalchemy import func
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
    all_franchises = Franchise.query.all()
    franchises = {franchise.id: franchise.name for franchise in all_franchises}
    avg_rating = db.session.query(func.avg(Review.review_rating))\
                          .filter(Review.user_id == current_user.id)\
                          .scalar() or 0
    
    # Get most visited franchise for the current user
    most_visited_query = db.session.query(
        Review.franchise_id, 
        func.count(Review.franchise_id).label('visit_count')
    ).filter(
        Review.user_id == current_user.id
    ).group_by(
        Review.franchise_id
    ).order_by(
        func.count(Review.franchise_id).desc()
    )
    
    most_visited_result = most_visited_query.first()
    
    if most_visited_result:
        most_visited_id = most_visited_result[0]
        visit_count = most_visited_result[1]
        most_visited_franchise = Franchise.query.get(most_visited_id)
    else:
        most_visited_franchise = None
        visit_count = 0

    return render_template('dashboard.html', franchises = franchises, avg_rating=avg_rating, 
                           most_visited_franchise=most_visited_franchise, visit_count=visit_count)

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