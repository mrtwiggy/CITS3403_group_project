# my_app/routes/main.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from my_app import db
from my_app.forms import ReviewForm
from my_app.models import Franchise, FranchiseLocation, Location, Review 
from datetime import datetime

reviews_bp = Blueprint('review', __name__)

# Routes for the review form
@reviews_bp.route('/reviews', methods=['GET'])
def reviews():
    form = ReviewForm()
    
    # Populate franchise dropdown with all available franchises
    franchises = Franchise.query.order_by(Franchise.name).all()
    form.franchise_id.choices = [(0, 'Select Franchise')] + [(f.id, f.name) for f in franchises]
    
    # Initially, the location dropdown is empty until franchise is selected
    form.location_id.choices = [(0, 'Select Location')]
    
    return render_template('create_review.html', form=form)

@reviews_bp.route('/api/franchise/<int:franchise_id>/locations')
def get_locations_for_franchise(franchise_id):
    # Get all franchise-location pairs for this franchise
    franchise_locations = FranchiseLocation.query.filter_by(
        franchise_id=franchise_id
    ).join(Location, FranchiseLocation.location_id == Location.id).all()
    
    # For a composite key model like yours, we need to return the composite key
    results = []
    for fl in franchise_locations:
        results.append({
            # We're creating a value that identifies this combination
            'id': f"{fl.franchise_id}_{fl.location_id}",  # Composite key as string
            'name': Location.query.get(fl.location_id).name
        })
    
    return jsonify(results)

@reviews_bp.route('/create_review', methods=['POST'])
def create_review():
    form = ReviewForm()
    
    # Dynamic loading of franchise locations for validation
    franchises = Franchise.query.order_by(Franchise.name).all()
    form.franchise_id.choices = [(0, 'Select Franchise')] + [(f.id, f.name) for f in franchises]

    # Extract franchise_id from submitted form
    franchise_id = form.franchise_id.data

    # Populate location choices based on selected franchise_id
    if franchise_id:
        franchise_locations = FranchiseLocation.query.filter_by(
            franchise_id=franchise_id
        ).join(Location, FranchiseLocation.location_id == Location.id).all()
        form.location_id.choices = [(fl.location_id, Location.query.get(fl.location_id).name) for fl in franchise_locations]
    else:
        form.location_id.choices = [(0, 'Select Location')]

    
    if form.validate_on_submit():
        # Get the franchise location to extract franchise_id and location_id
        franchise_id = form.franchise_id.data
        location_id = form.location_id.data  # This is now the location_id
        
        # Create the review with split franchise and location IDs
        new_review = Review(
            user_id=current_user.id,  # Add user ID
            franchise_id=franchise_id,  # Split from franchise_location
            location_id=location_id,    # Split from franchise_location

            drink_name=form.drink_name.data,
            drink_size=form.drink_size.data,
            review_content=form.review_content.data,

            sugar_level=form.sugar_level.data,
            ice_level=form.ice_level.data,
            review_rating=form.rating.data,  # Note: changed from rating to review_rating to match model
            uploaded_at=datetime.now()  # Add timestamp
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        flash('Your review has been submitted!', 'success')
        return redirect(url_for('main.recent_reviews'))
    
    # If validation fails
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", "error")
    
    return render_template('create_review.html', form=form)