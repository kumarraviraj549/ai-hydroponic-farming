"""Sensor readings routes for HydroAI API."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import SensorReading, Sensor, Farm
from datetime import datetime, timedelta
from sqlalchemy import and_, desc

readings_bp = Blueprint('readings', __name__)


@readings_bp.route('/farms/<int:farm_id>/readings', methods=['GET'])
@jwt_required()
def get_readings(farm_id):
    """Get sensor readings for a specific farm."""
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
        sensor_type = request.args.get('sensor_type')
        hours = int(request.args.get('hours', 24))  # Default last 24 hours
        limit = min(int(request.args.get('limit', 100)), 1000)  # Max 1000 readings
        
        # Build query
        query = SensorReading.query.filter_by(farm_id=farm_id)
        
        # Filter by time range
        since = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(SensorReading.timestamp >= since)
        
        # Filter by sensor type if specified
        if sensor_type:
            query = query.join(Sensor).filter(Sensor.sensor_type == sensor_type)
        
        # Order by timestamp and limit
        readings = query.order_by(desc(SensorReading.timestamp)).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [reading.to_dict() for reading in readings],
            'count': len(readings),
            'farm_id': farm_id,
            'time_range_hours': hours
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@readings_bp.route('/readings', methods=['POST'])
@jwt_required()
def create_reading():
    """Create a new sensor reading (for IoT devices)."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ('sensor_id', 'value')):
            return jsonify({
                'success': False,
                'error': 'Sensor ID and value are required'
            }), 400
        
        # Verify sensor exists and get farm_id
        sensor = Sensor.query.get(data['sensor_id'])
        if not sensor or not sensor.is_active:
            return jsonify({
                'success': False,
                'error': 'Sensor not found or inactive'
            }), 404
        
        # Verify farm ownership
        user_id = get_jwt_identity()
        if sensor.farm.user_id != user_id:
            return jsonify({
                'success': False,
                'error': 'Unauthorized access to sensor'
            }), 403
        
        # Create reading
        reading = SensorReading(
            sensor_id=data['sensor_id'],
            farm_id=sensor.farm_id,
            value=float(data['value']),
            timestamp=datetime.utcnow()
        )
        
        db.session.add(reading)
        db.session.commit()
        
        # Check if reading triggers any alerts (threshold monitoring)
        from services.alert_service import check_threshold_alerts
        check_threshold_alerts(reading)
        
        return jsonify({
            'success': True,
            'data': reading.to_dict(),
            'message': 'Reading recorded successfully'
        }), 201
        
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid value format'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@readings_bp.route('/farms/<int:farm_id>/readings/summary', methods=['GET'])
@jwt_required()
def get_readings_summary(farm_id):
    """Get aggregated readings summary for dashboard."""
    try:
        user_id = get_jwt_identity()
        
        # Verify farm ownership
        farm = Farm.query.filter_by(id=farm_id, user_id=user_id, is_active=True).first()
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Get latest reading for each sensor
        sensors = Sensor.query.filter_by(farm_id=farm_id, is_active=True).all()
        summary = []
        
        for sensor in sensors:
            latest_reading = SensorReading.query.filter_by(
                sensor_id=sensor.id
            ).order_by(desc(SensorReading.timestamp)).first()
            
            if latest_reading:
                summary.append({
                    'sensor_id': sensor.id,
                    'sensor_name': sensor.name,
                    'sensor_type': sensor.sensor_type,
                    'unit': sensor.unit,
                    'current_value': latest_reading.value,
                    'last_reading': latest_reading.timestamp.isoformat(),
                    'min_threshold': sensor.min_threshold,
                    'max_threshold': sensor.max_threshold,
                    'status': get_sensor_status(latest_reading.value, sensor)
                })
        
        return jsonify({
            'success': True,
            'data': summary,
            'farm_id': farm_id,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def get_sensor_status(value, sensor):
    """Determine sensor status based on thresholds."""
    if sensor.min_threshold is not None and value < sensor.min_threshold:
        return 'low'
    elif sensor.max_threshold is not None and value > sensor.max_threshold:
        return 'high'
    else:
        return 'normal'
