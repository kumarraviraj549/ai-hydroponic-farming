"""Alert service for threshold monitoring and notifications."""

from app import db
from models import Alert, Sensor, SensorReading
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def check_threshold_alerts(reading: SensorReading):
    """Check if a sensor reading triggers any threshold alerts."""
    try:
        sensor = reading.sensor
        
        if not sensor or not sensor.is_active:
            return
        
        alert_triggered = False
        alert_type = None
        severity = 'medium'
        message = ''
        
        # Check minimum threshold
        if sensor.min_threshold is not None and reading.value < sensor.min_threshold:
            alert_triggered = True
            alert_type = 'threshold'
            severity = 'high' if reading.value < (sensor.min_threshold * 0.8) else 'medium'
            message = f'{sensor.name} reading ({reading.value} {sensor.unit}) is below minimum threshold ({sensor.min_threshold} {sensor.unit})'
        
        # Check maximum threshold
        elif sensor.max_threshold is not None and reading.value > sensor.max_threshold:
            alert_triggered = True
            alert_type = 'threshold'
            severity = 'high' if reading.value > (sensor.max_threshold * 1.2) else 'medium'
            message = f'{sensor.name} reading ({reading.value} {sensor.unit}) is above maximum threshold ({sensor.max_threshold} {sensor.unit})'
        
        if alert_triggered:
            # Check if similar alert was recently created (avoid spam)
            recent_similar_alert = Alert.query.filter_by(
                farm_id=reading.farm_id,
                sensor_id=sensor.id,
                alert_type=alert_type,
                is_resolved=False
            ).filter(
                Alert.created_at > datetime.utcnow() - timedelta(hours=1)
            ).first()
            
            if not recent_similar_alert:
                # Create new alert
                alert = Alert(
                    farm_id=reading.farm_id,
                    sensor_id=sensor.id,
                    title=f'{sensor.sensor_type.title()} Alert - {sensor.name}',
                    message=message,
                    alert_type=alert_type,
                    severity=severity
                )
                
                db.session.add(alert)
                db.session.commit()
                
                logger.info(f"Created threshold alert for sensor {sensor.id}: {message}")
                
                # Send notifications if enabled
                send_alert_notifications(alert)
        
    except Exception as e:
        logger.error(f"Error checking threshold alerts: {str(e)}")
        db.session.rollback()


def send_alert_notifications(alert: Alert):
    """Send alert notifications via email and SMS."""
    try:
        from flask import current_app
        
        # Email notifications
        if current_app.config.get('ALERT_EMAIL_ENABLED', False):
            send_email_alert(alert)
        
        # SMS notifications
        if current_app.config.get('ALERT_SMS_ENABLED', False):
            send_sms_alert(alert)
            
    except Exception as e:
        logger.error(f"Error sending alert notifications: {str(e)}")


def send_email_alert(alert: Alert):
    """Send email alert notification."""
    # TODO: Implement email sending logic
    # This would typically use Flask-Mail or similar service
    logger.info(f"Email alert sent for alert {alert.id}")
    pass


def send_sms_alert(alert: Alert):
    """Send SMS alert notification."""
    # TODO: Implement SMS sending logic
    # This would typically use Twilio or similar service
    logger.info(f"SMS alert sent for alert {alert.id}")
    pass


def create_system_alert(farm_id: int, title: str, message: str, severity: str = 'medium'):
    """Create a system-generated alert."""
    try:
        alert = Alert(
            farm_id=farm_id,
            title=title,
            message=message,
            alert_type='system',
            severity=severity
        )
        
        db.session.add(alert)
        db.session.commit()
        
        logger.info(f"Created system alert for farm {farm_id}: {title}")
        
        # Send notifications for critical alerts
        if severity == 'critical':
            send_alert_notifications(alert)
            
        return alert
        
    except Exception as e:
        logger.error(f"Error creating system alert: {str(e)}")
        db.session.rollback()
        return None
