# Initialize the services package
# Import service instances
from .auth_service import auth_service
from .encryption_service import encryption_service
from .scheduler_service import scheduler_service
from .tiktok_api_service import tiktok_api_service

def init_app(app, db, jwt, scheduler, models):
    """Initialize all services with the app and dependencies"""
    # Create a services dictionary
    services = {
        'auth_service': auth_service,
        'encryption_service': encryption_service,
        'scheduler_service': scheduler_service,
        'tiktok_api_service': tiktok_api_service
    }
    
    # Initialize each service with its dependencies
    encryption_service.init_app(app)
    tiktok_api_service.init_app(app, encryption_service)
    auth_service.init_app(db, jwt, models['User'])
    scheduler_service.init_app(app, db, scheduler, models, services)
    
    return services