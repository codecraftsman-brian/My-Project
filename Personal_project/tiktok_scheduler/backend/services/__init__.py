# Initialize the services package
from .auth_service import AuthService
from .encryption_service import EncryptionService
from .scheduler_service import SchedulerService
from .tiktok_api_service import TikTokAPIService

# Create service instances
auth_service = AuthService()
encryption_service = EncryptionService()
scheduler_service = SchedulerService()
tiktok_api_service = TikTokAPIService()

def init_services(app):
    """Initialize services with app context"""
    encryption_service.init_app(app)
    scheduler_service.init_app(app)