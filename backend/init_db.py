#!/usr/bin/env python3
"""Database initialization script for HydroAI."""

import os
import sys
from app import create_app
from models import db, User, Farm, Sensor, SensorReading, Recommendation, Alert
from seed_demo_data import seed_demo_data
from datetime import datetime, timezone


def init_database(drop_existing=False):
    """Initialize the database with tables and optional demo data."""
    app = create_app()
    
    with app.app_context():
        try:
            if drop_existing:
                print("Dropping existing tables...")
                db.drop_all()
            
            print("Creating database tables...")
            db.create_all()
            
            # Check if we need to create demo user
            demo_mode = os.environ.get('DEMO_MODE', 'true').lower() == 'true'
            
            if demo_mode and not User.query.filter_by(email='demo@hydroai.com').first():
                print("Creating demo user...")
                # Get demo password from environment variable with fallback
                demo_password = os.environ.get('DEMO_PASSWORD', 'change_me_in_production')
                
                demo_user = User(
                    email='demo@hydroai.com',
                    name='Demo User',
                    company='HydroAI Demo',
                    phone='+1-555-0123'
                )
                demo_user.set_password(demo_password)
                db.session.add(demo_user)
                db.session.commit()
                
                print("Seeding demo data...")
                seed_demo_data()
            
            print("✅ Database initialized successfully!")
            print("\n📊 Database Summary:")
            print(f"   Users: {User.query.count()}")
            print(f"   Farms: {Farm.query.count()}")
            print(f"   Sensors: {Sensor.query.count()}")
            print(f"   Readings: {SensorReading.query.count()}")
            print(f"   Recommendations: {Recommendation.query.count()}")
            print(f"   Alerts: {Alert.query.count()}")
            
            if demo_mode:
                print("\n🔑 Demo Credentials:")
                print("   Email: demo@hydroai.com")
                print("   Password: [Set via DEMO_PASSWORD environment variable]")
                
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            db.session.rollback()
            sys.exit(1)


def check_database_connection():
    """Check if database connection is working."""
    app = create_app()
    
    with app.app_context():
        try:
            # Try to execute a simple query
            db.session.execute('SELECT 1')
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize HydroAI database')
    parser.add_argument('--drop', action='store_true', 
                       help='Drop existing tables before creating new ones')
    parser.add_argument('--check-connection', action='store_true',
                       help='Only check database connection')
    
    args = parser.parse_args()
    
    print("🌱 HydroAI Database Initialization")
    print("=" * 40)
    
    if args.check_connection:
        check_database_connection()
    else:
        if not check_database_connection():
            print("Please fix database connection issues before proceeding.")
            sys.exit(1)
        
        if args.drop:
            confirm = input("⚠️  This will delete all existing data. Continue? (y/N): ")
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                sys.exit(0)
        
        init_database(drop_existing=args.drop)