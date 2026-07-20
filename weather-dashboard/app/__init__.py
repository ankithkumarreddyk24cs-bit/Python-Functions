from flask import Flask
from flask_caching import Cache
from config import config

cache = Cache()

def create_app(config_name='development'):
    """
    Application factory function
    
    Args:
        config_name: Configuration environment
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize cache
    cache.init_app(app)
    
    # Register blueprints
    from app.routes.weather_routes import weather_bp
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    
    # Register web routes
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {'success': False, 'error': 'Internal server error'}, 500
    
    # Health check
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'success': True}, 200
    
    return app
