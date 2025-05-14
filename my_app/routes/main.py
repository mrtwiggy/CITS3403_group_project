# my_app/routes/main.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from my_app.forms import ReviewForm
from my_app.models import Franchise, Review, User, Friendship, Location
from sqlalchemy import func, or_, desc
from my_app import db 
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Get latest public reviews
    latest_reviews = db.session.query(Review).join(User).join(Franchise)\
        .filter(Review.is_private == False)\
        .order_by(Review.uploaded_at.desc())\
        .limit(3)\
        .all()

    # Get random selection of drinks from reviews
    trending_drinks = db.session.query(
        Review.drink_name,
        Franchise.name.label('franchise_name'),
        func.count(Review.id).label('review_count')
    ).join(Franchise)\
    .filter(Review.is_private == False)\
    .group_by(Review.drink_name, Franchise.name)\
    .order_by(func.random())\
    .limit(4)\
    .all()

    return render_template('index.html', 
                         latest_reviews=latest_reviews,
                         trending_drinks=trending_drinks)

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

    # Get pending friend requests
    friend_requests = current_user.received_friend_requests()
    
    # Get all friends
    friends = current_user.get_all_friends()

    # Get weekly activity data (last 7 days)
    today = datetime.now().date()
    week_dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    
    weekly_data = []
    weekly_labels = []
    
    for date in week_dates:
        count = Review.query.filter(
            Review.user_id == current_user.id,
            func.date(Review.uploaded_at) == date
        ).count()
        weekly_data.append(count)
        weekly_labels.append(date.strftime('%a'))  # Short day name (Mon, Tue, etc.)

    # Get franchise distribution data
    franchise_distribution = db.session.query(
        Franchise.name,
        func.count(Review.id).label('review_count')
    ).join(Review).filter(
        Review.user_id == current_user.id
    ).group_by(Franchise.name).all()

    franchise_labels = [fd[0] for fd in franchise_distribution]
    franchise_data = [fd[1] for fd in franchise_distribution]

    return render_template('dashboard.html', 
                         franchises=franchises, 
                         avg_rating=avg_rating,
                         most_visited_franchise=most_visited_franchise, 
                         visit_count=visit_count,
                         friend_requests=friend_requests,
                         friends=friends,
                         weekly_labels=weekly_labels,
                         weekly_data=weekly_data,
                         franchise_labels=franchise_labels,
                         franchise_data=franchise_data)

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

@main_bp.route('/api/get_reviews')
@login_required
def get_reviews():
    limit = request.args.get('limit', type=int)
    show_friends = request.args.get('friends', 'false') == 'true'
    
    # Base query for reviews with proper joins
    base_query = db.session.query(Review).join(
        User
    ).join(
        Franchise, Review.franchise_id == Franchise.id, isouter=True
    ).join(
        Location, Review.location_id == Location.id, isouter=True
    )
    
    if show_friends:
        # Get friend IDs
        friend_ids = [friend.id for friend in current_user.get_all_friends()]
        friend_ids.append(current_user.id)  # Include current user's reviews
        
        # Show all reviews (public and private) from friends
        base_query = base_query.filter(Review.user_id.in_(friend_ids))
    else:
        # Show only public reviews from everyone and all reviews from current user
        base_query = base_query.filter(
            or_(
                Review.is_private == False,
                Review.user_id == current_user.id
            )
        )
    
    # Order by most recent and limit if specified
    reviews = base_query.order_by(Review.uploaded_at.desc())
    if limit:
        reviews = reviews.limit(limit)
    else:
        reviews = reviews.limit(50)
    
    reviews = reviews.all()
    
    # Format reviews
    results = []
    for review in reviews:
        results.append({
            'id': review.id,
            'user': {
                'id': review.user.id,
                'username': review.user.username,
                'profile_pic': review.user.profile_pic
            },
            'franchise': {
                'id': review.franchise.id if review.franchise else None,
                'name': review.franchise.name if review.franchise else 'Unknown'
            },
            'location': {
                'id': review.location.id if review.location else None,
                'name': review.location.name if review.location else None,
                'address': review.location.address if review.location and hasattr(review.location, 'address') else None
            },
            'drink_name': review.drink_name,
            'drink_size': review.drink_size,
            'review_content': review.review_content,
            'sugar_level': review.sugar_level,
            'ice_level': review.ice_level,
            'rating': review.review_rating,
            'is_private': review.is_private,
            'uploaded_at': review.uploaded_at.isoformat(),
            'is_current_user': review.user_id == current_user.id
        })
    
    return jsonify(results)

@main_bp.route('/explore')
@login_required
def explore():
    return render_template('explore.html')

@main_bp.route('/api/search_users')
@login_required
def search_users():
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    # Search for users whose username contains the query
    users = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.id != current_user.id
    ).limit(5).all()
    
    # Format user data with friendship status
    results = []
    for user in users:
        # Check friendship status
        friendship = Friendship.query.filter(
            ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == user.id)) |
            ((Friendship.user1_id == user.id) & (Friendship.user2_id == current_user.id))
        ).first()
        
        friendship_status = 'none'
        if friendship:
            friendship_status = friendship.status
        
        results.append({
            'id': user.id,
            'username': user.username,
            'profile_pic': user.profile_pic,
            'friendship_status': friendship_status
        })
    
    return jsonify(results)

@main_bp.route('/api/trending_reviews')
@login_required
def get_trending_reviews():
    # Get 3 most recent reviews
    recent_reviews = Review.query.filter(
        or_(Review.is_private == False, Review.user_id == current_user.id)
    ).order_by(Review.uploaded_at.desc()).limit(3).all()
    
    # Get 3 most active users based on review count
    active_users = db.session.query(
        User,
        func.count(Review.id).label('review_count')
    ).join(Review).group_by(User.id).order_by(
        desc('review_count')
    ).limit(3).all()
    
    return jsonify({
        'recent_reviews': [{
            'id': review.id,
            'username': review.user.username,
            'drink_name': review.drink_name,
            'franchise_name': review.franchise.name if review.franchise else None,
            'rating': review.review_rating,
            'content': review.review_content,
            'uploaded_at': review.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        } for review in recent_reviews],
        'active_users': [{
            'username': user.username,
            'review_count': count,
            'profile_pic': user.profile_pic
        } for user, count in active_users]
    })

@main_bp.route('/api/leaderboard')
@login_required
def get_leaderboard():
    view_type = request.args.get('view', 'public')
    
    # Subquery to get each user's favorite franchise
    favorite_franchise_subq = db.session.query(
        Review.user_id,
        Franchise.name.label('franchise_name'),
        func.count().label('visit_count')
    ).join(
        Franchise, Review.franchise_id == Franchise.id
    ).group_by(
        Review.user_id,
        Franchise.name
    ).order_by(
        Review.user_id,
        func.count().desc()
    ).subquery()

    # Base query to get user stats
    base_query = db.session.query(
        User,
        func.count(Review.id).label('total_reviews'),
        func.first_value(favorite_franchise_subq.c.franchise_name).over(
            partition_by=User.id,
            order_by=favorite_franchise_subq.c.visit_count.desc()
        ).label('favorite_franchise')
    ).outerjoin(
        Review, User.id == Review.user_id
    ).outerjoin(
        favorite_franchise_subq, User.id == favorite_franchise_subq.c.user_id
    )
    
    if view_type == 'friends':
        # Get friend IDs
        friend_ids = [friend.id for friend in current_user.get_all_friends()]
        friend_ids.append(current_user.id)  # Include current user
        base_query = base_query.filter(User.id.in_(friend_ids))
    
    # Group and order results
    results = base_query.group_by(
        User.id,
        favorite_franchise_subq.c.franchise_name
    ).having(
        func.count(Review.id) > 0  # Only show users with reviews
    ).order_by(
        func.count(Review.id).desc()
    ).all()
    
    # Format results
    leaderboard = []
    for rank, (user, total_reviews, favorite_franchise) in enumerate(results, 1):
        leaderboard.append({
            'rank': rank,
            'user_id': user.id,
            'username': user.username,
            'profile_pic': user.profile_pic,
            'total_reviews': total_reviews,
            'favorite_franchise': favorite_franchise or 'No reviews yet',
            'is_current_user': user.id == current_user.id
        })
    
    # If current user is not in results and we're not in friends view, add them at the end
    if not any(entry['user_id'] == current_user.id for entry in leaderboard) and view_type != 'friends':
        # Get current user's stats
        user_stats = db.session.query(
            func.count(Review.id).label('total_reviews'),
            Franchise.name.label('favorite_franchise')
        ).outerjoin(
            Review, User.id == Review.user_id
        ).outerjoin(
            Franchise, Review.franchise_id == Franchise.id
        ).filter(
            User.id == current_user.id
        ).group_by(
            Franchise.name
        ).order_by(
            func.count(Review.id).desc()
        ).first()

        if user_stats:
            total_reviews, favorite_franchise = user_stats
        else:
            total_reviews, favorite_franchise = 0, None

        leaderboard.append({
            'rank': len(leaderboard) + 1,
            'user_id': current_user.id,
            'username': current_user.username,
            'profile_pic': current_user.profile_pic,
            'total_reviews': total_reviews,
            'favorite_franchise': favorite_franchise or 'No reviews yet',
            'is_current_user': True
        })
    
    return jsonify(leaderboard)

@main_bp.route('/api/active_users')
@login_required
def get_active_users():
    # Get users with their review counts, ordered by number of reviews
    active_users = db.session.query(
        User,
        func.count(Review.id).label('review_count')
    ).join(Review).group_by(User).order_by(
        func.count(Review.id).desc()
    ).limit(5).all()
    
    results = []
    for user, review_count in active_users:
        results.append({
            'id': user.id,
            'username': user.username,
            'profile_pic': user.profile_pic,
            'review_count': review_count
        })
    
    return jsonify(results)