# Initialize the routes package
from flask import Blueprint

# Export route setup functions
def create_blueprints():
    """Create all blueprints"""
    auth_bp = Blueprint('auth', __name__)
    scheduler_bp = Blueprint('scheduler', __name__)
    dashboard_bp = Blueprint('dashboard', __name__)
    
    return {
        'auth_bp': auth_bp,
        'scheduler_bp': scheduler_bp,
        'dashboard_bp': dashboard_bp
    }

def register_routes(blueprints, services, models):
    """Register routes with blueprints"""
    # Import route handlers
    from .auth_routes import register_auth_routes
    from .scheduler_routes import register_scheduler_routes
    from .dashboard_routes import register_dashboard_routes
    
    # Register routes with blueprints
    register_auth_routes(blueprints['auth_bp'], services, models)
    register_scheduler_routes(blueprints['scheduler_bp'], services, models)
    register_dashboard_routes(blueprints['dashboard_bp'], services, models)