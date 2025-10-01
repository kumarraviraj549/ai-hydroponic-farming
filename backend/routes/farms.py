"""Farm management routes for HydroAI API."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Farm, User, Sensor
from datetime import datetime

farms_bp = Blueprint('farms', __name__)


@farms_bp.route('/farms', methods=['GET'])
@jwt_required()
def get_farms():
    """Get all farms for authenticated user."""
    try:
        user_id = get_jwt_identity()
        farms = Farm.query.filter_by(user_id=user_id, is_active=True).all()
        
        return jsonify({
            'success': True,
            'data': [farm.to_dict() for farm in farms],
            'count': len(farms)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@farms_bp.route('/farms', methods=['POST'])
@jwt_required()
def create_farm():
    """Create a new farm."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name'):
            return jsonify({
                'success': False,
                'error': 'Farm name is required'
            }), 400
        
        # Create new farm
        farm = Farm(
            name=data['name'],
            description=data.get('description', ''),
            location=data.get('location', ''),
            size_sqft=data.get('size_sqft'),
            farm_type=data.get('farm_type', 'hydroponic'),
            user_id=user_id
        )
        
        db.session.add(farm)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': farm.to_dict(),
            'message': 'Farm created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@farms_bp.route('/farms/<int:farm_id>', methods=['GET'])
@jwt_required()
def get_farm(farm_id):
    """Get specific farm details."""
    try:
        user_id = get_jwt_identity()
        farm = Farm.query.filter_by(
            id=farm_id, 
            user_id=user_id, 
            is_active=True
        ).first()
        
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': farm.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@farms_bp.route('/farms/<int:farm_id>', methods=['PUT'])
@jwt_required()
def update_farm(farm_id):
    """Update farm information."""
    try:
        user_id = get_jwt_identity()
        farm = Farm.query.filter_by(
            id=farm_id, 
            user_id=user_id, 
            is_active=True
        ).first()
        
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        data = request.get_json()
        
        # Update farm fields
        if 'name' in data:
            farm.name = data['name']
        if 'description' in data:
            farm.description = data['description']
        if 'location' in data:
            farm.location = data['location']
        if 'size_sqft' in data:
            farm.size_sqft = data['size_sqft']
        if 'farm_type' in data:
            farm.farm_type = data['farm_type']
        
        farm.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': farm.to_dict(),
            'message': 'Farm updated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@farms_bp.route('/farms/<int:farm_id>', methods=['DELETE'])
@jwt_required()
def delete_farm(farm_id):
    """Soft delete a farm."""
    try:
        user_id = get_jwt_identity()
        farm = Farm.query.filter_by(
            id=farm_id, 
            user_id=user_id, 
            is_active=True
        ).first()
        
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        farm.is_active = False
        farm.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Farm deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
