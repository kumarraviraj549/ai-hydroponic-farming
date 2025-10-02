"""SQLAlchemy models for HydroAI application."""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize db here to avoid circular imports
db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and farm management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    farms = db.relationship('Farm', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'company': self.company,
            'phone': self.phone,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Farm(db.Model):
    """Farm model representing a hydroponic farming operation."""
    
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    size_sqft = db.Column(db.Integer)  # Farm size in square feet
    farm_type = db.Column(db.String(50))  # hydroponic, vertical, greenhouse
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    sensors = db.relationship('Sensor', backref='farm', lazy=True, cascade='all, delete-orphan')
    readings = db.relationship('SensorReading', backref='farm', lazy=True)
    recommendations = db.relationship('Recommendation', backref='farm', lazy=True)
    alerts = db.relationship('Alert', backref='farm', lazy=True)
    
    def to_dict(self):
        """Convert farm to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'size_sqft': self.size_sqft,
            'farm_type': self.farm_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sensor_count': len(self.sensors)
        }


class Sensor(db.Model):
    """Sensor model for monitoring environmental conditions."""
    
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)  # ph, temperature, humidity, nutrients
    unit = db.Column(db.String(20))  # pH, °C, %, ppm
    min_threshold = db.Column(db.Float)
    max_threshold = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Foreign keys
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    
    # Relationships
    readings = db.relationship('SensorReading', backref='sensor', lazy=True)
    
    def to_dict(self):
        """Convert sensor to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'sensor_type': self.sensor_type,
            'unit': self.unit,
            'min_threshold': self.min_threshold,
            'max_threshold': self.max_threshold,
            'is_active': self.is_active,
            'farm_id': self.farm_id
        }


class SensorReading(db.Model):
    """Sensor reading model for storing time-series data."""
    
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    
    # Foreign keys
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    
    def to_dict(self):
        """Convert reading to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'value': self.value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'sensor_id': self.sensor_id,
            'sensor_name': self.sensor.name if self.sensor else None,
            'sensor_type': self.sensor.sensor_type if self.sensor else None,
            'unit': self.sensor.unit if self.sensor else None
        }


class Recommendation(db.Model):
    """AI-generated recommendations for farm optimization."""
    
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    recommendation_type = db.Column(db.String(50))  # nutrient, ph, temperature, general
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    confidence_score = db.Column(db.Float)  # 0.0 to 1.0
    is_implemented = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Foreign keys
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    
    def to_dict(self):
        """Convert recommendation to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'recommendation_type': self.recommendation_type,
            'priority': self.priority,
            'confidence_score': self.confidence_score,
            'is_implemented': self.is_implemented,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'farm_id': self.farm_id
        }


class Alert(db.Model):
    """Alert model for critical conditions and notifications."""
    
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # threshold, system, prediction
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    is_read = db.Column(db.Boolean, default=False)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    resolved_at = db.Column(db.DateTime)
    
    # Foreign keys
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))  # Optional: specific sensor
    
    def to_dict(self):
        """Convert alert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'is_read': self.is_read,
            'is_resolved': self.is_resolved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'farm_id': self.farm_id,
            'sensor_id': self.sensor_id
        }