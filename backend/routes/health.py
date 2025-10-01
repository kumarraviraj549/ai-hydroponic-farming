"""Health check routes for HydroAI API."""

from flask import Blueprint, jsonify
from datetime import datetime
import os

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'HydroAI API',
        'version': '1.0.0'
    }), 200


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with system information."""
    try:
        # Test database connection
        from app import db
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy' if db_status == 'connected' else 'unhealthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'HydroAI API',
        'version': '1.0.0',
        'environment': os.environ.get('FLASK_ENV', 'development'),
        'database': db_status,
        'uptime': 'Not implemented yet'
    }), 200 if db_status == 'connected' else 503


@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """Kubernetes readiness probe endpoint."""
    try:
        from app import db
        db.session.execute('SELECT 1')
        return jsonify({'status': 'ready'}), 200
    except Exception:
        return jsonify({'status': 'not ready'}), 503


@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """Kubernetes liveness probe endpoint."""
    return jsonify({'status': 'alive'}), 200
