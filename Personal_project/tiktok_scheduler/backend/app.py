from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///tiktok_scheduler.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Import routes after app is initialized to avoid circular imports
from routes.auth_routes import auth_bp
from routes.scheduler_routes import scheduler_bp
from routes.dashboard_routes import dashboard_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(scheduler_bp, url_prefix='/api/scheduler')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    # Ensure all tables are created
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=True)