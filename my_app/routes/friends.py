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

@friend_bp.route('/request/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    user = User.query.get_or_404(user_id)

    if current_user.id == user.id:
        flash("You can't friend yourself.", "warning")
        return redirect(url_for('friends.friends_list'))

    if current_user.has_friend_requests_pending(user):
        flash("Friend request already sent.", "warning")

    elif current_user.is_friend_with(user):
        flash("You are already friends.", "warning")

    else:
        new_friend = Friendship(
            user1_id = current_user.id,
            user2_id = user.id,
            status = 'pending'
        )


        db.session.add(new_friend)
        db.session.commit()

    return redirect(url_for('main.explore'))

@friend_bp.route('accept/<int:user_id>', methods=['POST'])
@login_required
def accept_friend(user_id):
    sender = User.query.get_or_404(user_id)

    if not sender:
        return jsonify({"error": "User not found"}), 404

    pending_request = Friendship.query.filter(
        (Friendship.user1_id == sender.id) &
        (Friendship.user2_id == current_user.id) &
        (Friendship.status == 'pending')
    ).first()  # Use .first() to get a single result

    if pending_request:
        # Update the status to 'accepted'
        pending_request.status = 'accepted'
        db.session.commit()  # Save the changes to the database
        return jsonify({"message": "Friend request accepted"})
    else:
        return jsonify({"error": "No pending request found"}), 400


@friend_bp.route('/reject/<int:user_id>', methods=['POST'])
@login_required
def reject_request(user_id):
    sender = User.query.get_or_404(user_id)

    if not sender:
        return jsonify({"error": "User not found"}), 404

    pending_request = Friendship.query.filter(
        (Friendship.user1_id == sender.id) &
        (Friendship.user2_id == current_user.id) &
        (Friendship.status == 'pending')
    ).first()  # Use .first() to get a single result

    if pending_request:
        # Update the status to 'accepted'
        db.session.delete(pending_request)
        db.session.commit()  # Save the changes to the database
        return jsonify({"message": "Friend request rejected"})
    else:
        return jsonify({"error": "No pending request found"}), 400

@friend_bp.route('/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    """Remove a friend"""
    sender = User.query.get_or_404(user_id)

    if not sender:
        return jsonify({"error": "User not found"}), 404

    pending_request = Friendship.query.filter(
        (((Friendship.user1_id == sender.id) & (Friendship.user2_id == current_user.id)) |
        ((Friendship.user1_id == current_user.id) & (Friendship.user2_id == sender.id))) &
        (Friendship.status == 'accepted')
    ).first()  # Use .first() to get a single result

    if pending_request:
        # Update the status to 'accepted'
        db.session.delete(pending_request)
        db.session.commit()  # Save the changes to the database
        return jsonify({"message": "Friend relation removed"})
    else:
        return jsonify({"error": "No pending request found"}), 400

