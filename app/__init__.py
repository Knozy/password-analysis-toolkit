
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime
from app.core.password_analyzer import PasswordAnalyzer
db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_analysis.db'
        app.config['DEBUG'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_analysis_prod.db'
        app.config['DEBUG'] = False
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from app.routes import web_routes
    app.register_blueprint(web_routes.bp)
    from app.routes import auth_routes, analysis_routes, attack_routes, report_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(analysis_routes.bp)
    app.register_blueprint(attack_routes.bp)
    app.register_blueprint(report_routes.bp)
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app


# app/main.py
from app import create_app, db
import logging

app = create_app('development')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',  # Localhost only
        port=5000,
        debug=True,
        use_reloader=True
    )
