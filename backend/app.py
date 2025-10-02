"""Main Flask application factory for HydroAI backend."""

import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the database instance from models
from models import db

# Initialize other extensions
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS for frontend
    CORS(app, origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",  # Alternative localhost
        "https://hydroai.com",    # Production domain
    ], supports_credentials=True)
    
    # Import models to ensure they are registered with SQLAlchemy
    from models import User, Farm, Sensor, SensorReading, Recommendation, Alert
    
    # Register blueprints
    from routes.health import health_bp
    from routes.farms import farms_bp
    from routes.readings import readings_bp
    from routes.recommendations import recommendations_bp
    from routes.alerts import alerts_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    app.register_blueprint(farms_bp, url_prefix='/api/v1')
    app.register_blueprint(readings_bp, url_prefix='/api/v1')
    app.register_blueprint(recommendations_bp, url_prefix='/api/v1')
    app.register_blueprint(alerts_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    
    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'message': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'message': 'Token is required'}, 401
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'message': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'message': 'Bad request'}, 400
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)