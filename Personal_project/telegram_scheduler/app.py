#!/usr/bin/env python3
"""
Main entry point for the Telegram Message Scheduler application.
This file initializes and runs the Flask web application.
"""

import os
from datetime import datetime
from flask import Flask
from config import Config
from scheduler import create_scheduler
from web import register_routes

def create_app():
    """Create and configure the Flask application."""
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)
    
    # Ensure required config keys exist before using them
    if not hasattr(app, 'config') or 'DATA_DIR' not in app.config:
        # Default configuration if not loaded properly
        app.config['DATA_DIR'] = os.path.join(os.path.dirname(__file__), 'data')
        app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
        app.config['CONFIG_FILE'] = os.path.join(app.config['DATA_DIR'], 'config.json')
        app.config['MESSAGE_FILE'] = os.path.join(app.config['DATA_DIR'], 'messages.json')
        app.config['SENT_LOG_FILE'] = os.path.join(app.config['DATA_DIR'], 'sent_log.json')
        app.config['SECRET_KEY'] = 'telegram_scheduler_secret_key'
    
    # Create data directories
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize scheduler
    app.scheduler = create_scheduler(app.config['DATA_DIR'])
    
    # Register routes
    register_routes(app)
    
    # Make current date available to templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("===================================================")
    print("Telegram Message Scheduler")
    print("===================================================")
    print("This application allows you to schedule and send random")
    print("messages to random Telegram users, groups, or channels.")
    print("")
    print("Requirements:")
    print("1. Python packages: flask, telethon, werkzeug")
    print("2. Telegram API credentials (get from https://my.telegram.org/apps)")
    print("")
    print("Starting server...")
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=8080)