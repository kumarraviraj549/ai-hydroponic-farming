"""Alert management routes for HydroAI API."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Alert, Farm
from datetime import datetime, timedelta
from sqlalchemy import desc

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('/farms/<int:farm_id>/alerts', methods=['GET'])
@jwt_required()
def get_alerts(farm_id):
    """Get alerts for a specific farm."""
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
        is_read = request.args.get('is_read')
        is_resolved = request.args.get('is_resolved')
        severity = request.args.get('severity')
        days = int(request.args.get('days', 7))  # Default last 7 days
        limit = min(int(request.args.get('limit', 50)), 200)
        
        # Build query
        query = Alert.query.filter_by(farm_id=farm_id)
        
        # Filter by time range
        since = datetime.utcnow() - timedelta(days=days)
        query = query.filter(Alert.created_at >= since)
        
        # Apply filters
        if is_read is not None:
            query = query.filter_by(is_read=is_read.lower() == 'true')
        
        if is_resolved is not None:
            query = query.filter_by(is_resolved=is_resolved.lower() == 'true')
        
        if severity:
            query = query.filter_by(severity=severity)
        
        alerts = query.order_by(desc(Alert.created_at)).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [alert.to_dict() for alert in alerts],
            'count': len(alerts),
            'farm_id': farm_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@alerts_bp.route('/alerts/<int:alert_id>/read', methods=['PUT'])
@jwt_required()
def mark_alert_read(alert_id):
    """Mark an alert as read."""
    try:
        user_id = get_jwt_identity()
        
        # Find alert and verify ownership
        alert = Alert.query.join(Farm).filter(
            Alert.id == alert_id,
            Farm.user_id == user_id
        ).first()
        
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
        
        alert.is_read = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': alert.to_dict(),
            'message': 'Alert marked as read'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@alerts_bp.route('/alerts/<int:alert_id>/resolve', methods=['PUT'])
@jwt_required()
def resolve_alert(alert_id):
    """Mark an alert as resolved."""
    try:
        user_id = get_jwt_identity()
        
        # Find alert and verify ownership
        alert = Alert.query.join(Farm).filter(
            Alert.id == alert_id,
            Farm.user_id == user_id
        ).first()
        
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
        
        alert.is_resolved = True
        alert.resolved_at = datetime.utcnow()
        alert.is_read = True  # Mark as read when resolved
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': alert.to_dict(),
            'message': 'Alert resolved successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@alerts_bp.route('/farms/<int:farm_id>/alerts/summary', methods=['GET'])
@jwt_required()
def get_alerts_summary(farm_id):
    """Get alert summary statistics for dashboard."""
    try:
        user_id = get_jwt_identity()
        
        # Verify farm ownership
        farm = Farm.query.filter_by(id=farm_id, user_id=user_id, is_active=True).first()
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Count alerts by status
        total_alerts = Alert.query.filter_by(farm_id=farm_id).count()
        unread_alerts = Alert.query.filter_by(farm_id=farm_id, is_read=False).count()
        unresolved_alerts = Alert.query.filter_by(farm_id=farm_id, is_resolved=False).count()
        critical_alerts = Alert.query.filter_by(
            farm_id=farm_id, 
            severity='critical', 
            is_resolved=False
        ).count()
        
        # Recent alerts (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(hours=24)
        recent_alerts = Alert.query.filter(
            Alert.farm_id == farm_id,
            Alert.created_at >= yesterday
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_alerts': total_alerts,
                'unread_alerts': unread_alerts,
                'unresolved_alerts': unresolved_alerts,
                'critical_alerts': critical_alerts,
                'recent_alerts_24h': recent_alerts
            },
            'farm_id': farm_id,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
