from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__)

# Placeholder logic – no actual DB users table yet
@users_bp.route('/', methods=['GET'])
def get_users():
    return jsonify([{'id': 1, 'username': 'testuser'}])

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id == 1:
        return jsonify({'id': 1, 'username': 'testuser'})
    return jsonify({'message': 'User not found'}), 404
