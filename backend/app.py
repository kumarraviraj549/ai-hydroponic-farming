"""Main Flask application factory for HydroAI backend."""

import os
import logging
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Initialize extensions
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
    
    # Import db from models after app config is set
    from models import db
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Enable CORS for frontend
    CORS(app, origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",  # Alternative localhost
        "https://hydroai.com",    # Production domain
    ], supports_credentials=True)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created successfully")
    
    # Setup error handlers
    setup_error_handlers(app)
    
    return app


def register_blueprints(app):
    """Register all application blueprints."""
    from routes.health import health_bp
    from routes.farms import farms_bp
    from routes.readings import readings_bp
    from routes.recommendations import recommendations_bp
    from routes.alerts import alerts_bp
    from routes.auth import auth_bp
    from routes.reports import reports_bp
    
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    app.register_blueprint(farms_bp, url_prefix='/api/v1')
    app.register_blueprint(readings_bp, url_prefix='/api/v1')
    app.register_blueprint(recommendations_bp, url_prefix='/api/v1')
    app.register_blueprint(alerts_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(reports_bp)  # already has /api/v1 prefix in blueprint


def setup_logging(app):
    """Setup application logging."""
    if not app.debug and not app.testing:
        # Setup file logging for production
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/hydroai.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('HydroAI startup')


def setup_error_handlers(app):
    """Setup global error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'success': False, 'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from models import db
        db.session.rollback()
        app.logger.error(f'Server Error: {error}')
        return {'success': False, 'error': 'Internal server error'}, 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return {'success': False, 'error': 'Forbidden'}, 403
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return {'success': False, 'error': 'Unauthorized'}, 401


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
