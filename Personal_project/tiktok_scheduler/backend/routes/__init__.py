# Initialize the routes package
from flask import Blueprint

# Create blueprint instances
auth_bp = Blueprint('auth', __name__)
scheduler_bp = Blueprint('scheduler', __name__)
dashboard_bp = Blueprint('dashboard', __name__)

# Import routes to register them with blueprints
from . import auth_routes
from . import scheduler_routes
from . import dashboard_routes