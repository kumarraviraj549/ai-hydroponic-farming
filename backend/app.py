"""Main Flask application factory for HydroAI backend."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
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
        "https://hydroai.com",    # Production domain
    ])
    
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
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
