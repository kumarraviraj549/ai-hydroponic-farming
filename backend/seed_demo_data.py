#!/usr/bin/env python3
"""Seed demo data for HydroAI application."""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import User, Farm, Sensor, SensorReading, Recommendation, Alert


def seed_demo_data():
    """Seed the database with demo data."""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create demo user
        print("Creating demo user...")
        # Get demo password from environment variable with fallback
        demo_password = os.environ.get('DEMO_PASSWORD', 'change_me_in_production')
        
        demo_user = User(
            email='demo@hydroai.com',
            name='Demo User',
            company='HydroAI Demo Farm',
            phone='+1-555-123-4567'
        )
        demo_user.set_password(demo_password)
        db.session.add(demo_user)
        db.session.commit()
        
        # Create demo farms
        print("Creating demo farms...")
        farms_data = [
            {
                'name': 'Tomato Greenhouse A',
                'description': 'Main tomato production facility with climate control',
                'location': 'Sector 1, Building A',
                'size_sqft': 2500,
                'farm_type': 'greenhouse'
            },
            {
                'name': 'Lettuce Vertical Farm',
                'description': 'Multi-level lettuce growing system with LED lighting',
                'location': 'Sector 2, Building B',
                'size_sqft': 1200,
                'farm_type': 'vertical'
            },
            {
                'name': 'Herbs Hydroponic Unit',
                'description': 'Specialized unit for basil, mint and cilantro production',
                'location': 'Sector 3, Building C',
                'size_sqft': 800,
                'farm_type': 'hydroponic'
            }
        ]
        
        farms = []
        for farm_data in farms_data:
            farm = Farm(user_id=demo_user.id, **farm_data)
            farms.append(farm)
            db.session.add(farm)
        
        db.session.commit()
        
        # Create sensors for each farm
        print("Creating sensors...")
        sensor_types = [
            {'type': 'temperature', 'unit': '°C', 'min_threshold': 18.0, 'max_threshold': 28.0},
            {'type': 'humidity', 'unit': '%', 'min_threshold': 50.0, 'max_threshold': 80.0},
            {'type': 'ph', 'unit': 'pH', 'min_threshold': 5.5, 'max_threshold': 7.0},
            {'type': 'nutrients', 'unit': 'ppm', 'min_threshold': 800.0, 'max_threshold': 1200.0}
        ]
        
        sensors = []
        for i, farm in enumerate(farms):
            for j, sensor_type in enumerate(sensor_types):
                sensor = Sensor(
                    name=f"{sensor_type['type'].title()} Sensor {i+1}-{j+1}",
                    sensor_type=sensor_type['type'],
                    unit=sensor_type['unit'],
                    min_threshold=sensor_type['min_threshold'],
                    max_threshold=sensor_type['max_threshold'],
                    farm_id=farm.id
                )
                sensors.append(sensor)
                db.session.add(sensor)
        
        db.session.commit()
        
        # Generate sensor readings for the last 7 days
        print("Generating sensor readings...")
        now = datetime.utcnow()
        
        for sensor in sensors:
            for hours_ago in range(168, 0, -1):  # 7 days * 24 hours
                timestamp = now - timedelta(hours=hours_ago)
                
                # Generate realistic values based on sensor type
                if sensor.sensor_type == 'temperature':
                    base_value = 22 + random.gauss(0, 1)
                    # Add daily cycle
                    hour_of_day = timestamp.hour
                    daily_variation = 2 * (0.5 - abs(hour_of_day - 12) / 24)
                    value = base_value + daily_variation + random.gauss(0, 0.5)
                elif sensor.sensor_type == 'humidity':
                    value = 65 + random.gauss(0, 5)
                elif sensor.sensor_type == 'ph':
                    value = 6.2 + random.gauss(0, 0.2)
                elif sensor.sensor_type == 'nutrients':
                    value = 950 + random.gauss(0, 50)
                else:
                    value = random.uniform(0, 100)
                
                # Ensure value is within reasonable bounds
                value = max(0, value)
                
                reading = SensorReading(
                    value=round(value, 2),
                    timestamp=timestamp,
                    sensor_id=sensor.id,
                    farm_id=sensor.farm_id
                )
                db.session.add(reading)
        
        db.session.commit()
        
        # Create demo recommendations
        print("Creating recommendations...")
        recommendations_data = [
            {
                'title': 'Optimize Nutrient Levels',
                'description': 'Current nutrient levels are slightly below optimal. Consider increasing nutrient concentration by 5% to improve plant growth.',
                'recommendation_type': 'nutrient',
                'priority': 'medium',
                'confidence_score': 0.85,
                'farm_id': farms[0].id
            },
            {
                'title': 'Temperature Control Adjustment',
                'description': 'Temperature fluctuations detected. Recommend adjusting HVAC settings to maintain more stable temperatures.',
                'recommendation_type': 'temperature',
                'priority': 'high',
                'confidence_score': 0.92,
                'farm_id': farms[1].id
            },
            {
                'title': 'pH Buffer Optimization',
                'description': 'pH levels are stable but could be optimized for better nutrient uptake. Consider slight adjustment to 6.0.',
                'recommendation_type': 'ph',
                'priority': 'low',
                'confidence_score': 0.78,
                'farm_id': farms[2].id
            }
        ]
        
        for rec_data in recommendations_data:
            recommendation = Recommendation(**rec_data)
            db.session.add(recommendation)
        
        db.session.commit()
        
        # Create demo alerts
        print("Creating alerts...")
        alerts_data = [
            {
                'title': 'pH Level Critical',
                'message': 'Tomato Greenhouse A - pH dropped to 4.8, immediate attention required',
                'alert_type': 'threshold',
                'severity': 'critical',
                'farm_id': farms[0].id,
                'created_at': now - timedelta(minutes=30)
            },
            {
                'title': 'Temperature High Alert',
                'message': 'Lettuce Vertical Farm - Temperature reached 29°C, check cooling system',
                'alert_type': 'threshold',
                'severity': 'high',
                'farm_id': farms[1].id,
                'created_at': now - timedelta(hours=2)
            },
            {
                'title': 'Nutrient Level Low',
                'message': 'Herbs Hydroponic Unit - Nutrient solution at 750 ppm, consider refilling',
                'alert_type': 'threshold',
                'severity': 'medium',
                'farm_id': farms[2].id,
                'created_at': now - timedelta(hours=6),
                'is_read': True
            }
        ]
        
        for alert_data in alerts_data:
            alert = Alert(**alert_data)
            db.session.add(alert)
        
        db.session.commit()
        
        print("\n✓ Demo data seeded successfully!")
        print(f"Created:")
        print(f"  - 1 demo user (demo@hydroai.com / [DEMO_PASSWORD env var])")
        print(f"  - {len(farms)} farms")
        print(f"  - {len(sensors)} sensors")
        print(f"  - {len(sensors) * 168} sensor readings (7 days)")
        print(f"  - {len(recommendations_data)} recommendations")
        print(f"  - {len(alerts_data)} alerts")
        print("\nYou can now start the application and login with demo credentials.")


if __name__ == '__main__':
    seed_demo_data()