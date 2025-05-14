from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from my_app.models import User, Friendship, db 

friend_bp = Blueprint('friends', __name__)

@friend_bp.route('/friends')
@login_required
def friends_list():
    """Show list of friends and pending requests"""
    friends = current_user.get_all_friends()
    pending_sent = current_user.sent_friend_requests.filter_by(status='pending').all()
    pending_received = current_user.received_friend_requests.filter_by(status='pending').all()
    
    return render_template('friends/list.html',
                         friends=friends,
                         pending_sent=pending_sent,
                         pending_received=pending_received)

@friend_bp.route('/friends/search')
@login_required
def search_users():
    """Search for users to add as friends"""
    query = request.args.get('q', '').strip()
    if query:
        users = User.query.filter(
            User.username.ilike(f'%{query}%'),
            User.id != current_user.id
        ).all()
    else:
        users = []
    
    return render_template('friends/search.html', users=users, query=query)

@friend_bp.route('/friends/request/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    """Send a friend request"""
    user = User.query.get_or_404(user_id)
    
    # Check if request is AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if current_user.has_friend_requests_pending(user):
        message = 'Friend request already pending.'
        if is_ajax:
            return jsonify({'status': 'error', 'message': message}), 400
        flash(message, 'warning')
    elif current_user.is_friend_with(user):
        message = 'You are already friends.'
        if is_ajax:
            return jsonify({'status': 'error', 'message': message}), 400
        flash(message, 'warning')
    else:
        friendship = current_user.send_friend_request(user)
        if friendship:
            db.session.commit()
            message = f'Friend request sent to {user.username}!'
            if is_ajax:
                return jsonify({'status': 'success', 'message': message})
            flash(message, 'success')
        else:
            message = 'Could not send friend request.'
            if is_ajax:
                return jsonify({'status': 'error', 'message': message}), 400
            flash(message, 'error')
    
    if is_ajax:
        return jsonify({'status': 'error', 'message': 'Unknown error'}), 400
    return redirect(url_for('friends.friends_list'))

@friend_bp.route('/friends/accept/<int:user_id>', methods=['POST'])
@login_required
def accept_request(user_id):
    """Accept a friend request"""
    user = User.query.get_or_404(user_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if current_user.accept_friend_request(user):
        db.session.commit()
        message = f'You are now friends with {user.username}!'
        if is_ajax:
            return jsonify({'status': 'success', 'message': message})
        flash(message, 'success')
    else:
        message = 'No pending request found.'
        if is_ajax:
            return jsonify({'status': 'error', 'message': message}), 400
        flash(message, 'error')
    
    if is_ajax:
        return jsonify({'status': 'error', 'message': 'Unknown error'}), 400
    return redirect(url_for('friends.friends_list'))

@friend_bp.route('/friends/reject/<int:user_id>', methods=['POST'])
@login_required
def reject_request(user_id):
    """Reject a friend request"""
    user = User.query.get_or_404(user_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if current_user.reject_friend_request(user):
        db.session.commit()
        message = f'Friend request from {user.username} rejected.'
        if is_ajax:
            return jsonify({'status': 'success', 'message': message})
        flash(message, 'info')
    else:
        message = 'No pending request found.'
        if is_ajax:
            return jsonify({'status': 'error', 'message': message}), 400
        flash(message, 'error')
    
    if is_ajax:
        return jsonify({'status': 'error', 'message': 'Unknown error'}), 400
    return redirect(url_for('friends.friends_list'))

@friend_bp.route('/friends/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    """Remove a friend"""
    user = User.query.get_or_404(user_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if current_user.is_friend_with(user):
        current_user.remove_friend(user)
        db.session.commit()
        message = f'Removed {user.username} from friends.'
        if is_ajax:
            return jsonify({'status': 'success', 'message': message})
        flash(message, 'info')
    else:
        message = 'You are not friends with this user.'
        if is_ajax:
            return jsonify({'status': 'error', 'message': message}), 400
        flash(message, 'error')
    
    if is_ajax:
        return jsonify({'status': 'error', 'message': 'Unknown error'}), 400
    return redirect(url_for('friends.friends_list'))
