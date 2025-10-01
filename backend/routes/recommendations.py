"""Recommendations routes for HydroAI API."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Recommendation, Farm, SensorReading, Sensor
from datetime import datetime, timedelta
from ml_models.nutrient_predictor import NutrientPredictor

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/farms/<int:farm_id>/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations(farm_id):
    """Get AI recommendations for a specific farm."""
    try:
        user_id = get_jwt_identity()
        
        # Verify farm ownership
        farm = Farm.query.filter_by(id=farm_id, user_id=user_id, is_active=True).first()
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Query parameters
        implemented = request.args.get('implemented')
        priority = request.args.get('priority')
        limit = min(int(request.args.get('limit', 20)), 100)
        
        # Build query
        query = Recommendation.query.filter_by(farm_id=farm_id)
        
        if implemented is not None:
            query = query.filter_by(is_implemented=implemented.lower() == 'true')
        
        if priority:
            query = query.filter_by(priority=priority)
        
        recommendations = query.order_by(
            Recommendation.priority.desc(),
            Recommendation.created_at.desc()
        ).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [rec.to_dict() for rec in recommendations],
            'count': len(recommendations),
            'farm_id': farm_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recommendations_bp.route('/farms/<int:farm_id>/recommendations/generate', methods=['POST'])
@jwt_required()
def generate_recommendations(farm_id):
    """Generate new AI recommendations based on current sensor data."""
    try:
        user_id = get_jwt_identity()
        
        # Verify farm ownership
        farm = Farm.query.filter_by(id=farm_id, user_id=user_id, is_active=True).first()
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Get recent sensor data for AI analysis
        recent_readings = get_recent_sensor_data(farm_id)
        
        if not recent_readings:
            return jsonify({
                'success': False,
                'error': 'No recent sensor data available for analysis'
            }), 400
        
        # Initialize ML predictor
        predictor = NutrientPredictor()
        
        # Generate recommendations
        recommendations = predictor.predict(recent_readings)
        
        # Save recommendations to database
        saved_recommendations = []
        for rec_data in recommendations:
            recommendation = Recommendation(
                farm_id=farm_id,
                title=rec_data['title'],
                description=rec_data['description'],
                recommendation_type=rec_data['type'],
                priority=rec_data['priority'],
                confidence_score=rec_data['confidence']
            )
            
            db.session.add(recommendation)
            saved_recommendations.append(recommendation)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': [rec.to_dict() for rec in saved_recommendations],
            'count': len(saved_recommendations),
            'message': f'Generated {len(saved_recommendations)} new recommendations'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@recommendations_bp.route('/recommendations/<int:rec_id>/implement', methods=['PUT'])
@jwt_required()
def mark_recommendation_implemented(rec_id):
    """Mark a recommendation as implemented."""
    try:
        user_id = get_jwt_identity()
        
        # Find recommendation and verify ownership
        recommendation = Recommendation.query.join(Farm).filter(
            Recommendation.id == rec_id,
            Farm.user_id == user_id
        ).first()
        
        if not recommendation:
            return jsonify({
                'success': False,
                'error': 'Recommendation not found'
            }), 404
        
        recommendation.is_implemented = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': recommendation.to_dict(),
            'message': 'Recommendation marked as implemented'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def get_recent_sensor_data(farm_id, hours=24):
    """Get recent sensor readings for ML analysis."""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    readings = db.session.query(
        SensorReading.value,
        SensorReading.timestamp,
        Sensor.sensor_type,
        Sensor.unit
    ).join(Sensor).filter(
        SensorReading.farm_id == farm_id,
        SensorReading.timestamp >= since,
        Sensor.is_active == True
    ).order_by(SensorReading.timestamp.desc()).all()
    
    # Convert to dictionary format for ML model
    sensor_data = {}
    for reading in readings:
        if reading.sensor_type not in sensor_data:
            sensor_data[reading.sensor_type] = []
        
        sensor_data[reading.sensor_type].append({
            'value': reading.value,
            'timestamp': reading.timestamp.isoformat(),
            'unit': reading.unit
        })
    
    return sensor_data
