"""Authentication routes for HydroAI API."""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import db, User
from datetime import datetime, timezone
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ('email', 'password', 'name')):
            return jsonify({
                'success': False,
                'error': 'Email, password, and name are required'
            }), 400
        
        # Validate email format
        if '@' not in data['email'] or '.' not in data['email']:
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # Validate password strength
        if len(data['password']) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters long'
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email'].lower()).first():
            return jsonify({
                'success': False,
                'error': 'User with this email already exists'
            }), 409
        
        # Create new user
        user = User(
            email=data['email'].lower(),
            name=data['name'].strip(),
            company=data.get('company', '').strip(),
            phone=data.get('phone', '').strip()
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        logger.info(f'New user registered: {user.email}')
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Registration error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Registration failed. Please try again.'
        }), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT tokens."""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Find user (case-insensitive email)
        user = User.query.filter_by(email=data['email'].lower()).first()
        
        if not user or not user.check_password(data['password']):
            logger.warning(f'Failed login attempt for: {data.get("email", "unknown")}')
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated. Please contact support.'
            }), 401
        
        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        logger.info(f'Successful login: {user.email}')
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500


@auth_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token."""
    try:
        current_user_id = get_jwt_identity()
        
        # Verify user still exists and is active
        user = User.query.get(current_user_id)
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Invalid user or account deactivated'
            }), 401
        
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'access_token': new_access_token
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Token refresh error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Token refresh failed'
        }), 500


@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 401
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f'Get profile error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to fetch profile'
        }), 500


@auth_bp.route('/auth/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile."""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Update user fields
        if 'name' in data and data['name'].strip():
            user.name = data['name'].strip()
        if 'company' in data:
            user.company = data['company'].strip()
        if 'phone' in data:
            user.phone = data['phone'].strip()
        
        user.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        logger.info(f'Profile updated: {user.email}')
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Profile update error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Profile update failed'
        }), 500