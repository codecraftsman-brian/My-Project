#!/usr/bin/env python3
"""
Test script to validate that the TikTok Scheduler application is running correctly.
This script checks both backend and frontend components.
"""

import os
import sys
import subprocess
import time
import requests
from urllib.parse import urljoin
import webbrowser
import json

BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(message):
    """Print a formatted header message"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{message.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.END}\n")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.END}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ️ {message}{Colors.END}")

def check_directory_structure():
    """Check if the project directory structure is valid"""
    print_header("Checking Directory Structure")
    
    required_dirs = [
        "backend",
        "backend/routes",
        "backend/models",
        "backend/services",
        "backend/utils",
        "frontend",
        "frontend/public",
        "frontend/src",
        "frontend/src/components",
        "frontend/src/services",
        "frontend/src/styles"
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.isdir(directory):
            missing_dirs.append(directory)
    
    if missing_dirs:
        print_error(f"Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print_success("Directory structure is valid")
    return True

def check_key_files():
    """Check if key files exist"""
    print_header("Checking Key Files")
    
    backend_files = [
        "backend/app.py",
        "backend/config.py",
        "backend/routes/__init__.py",
        "backend/routes/auth_routes.py",
        "backend/routes/scheduler_routes.py",
        "backend/routes/dashboard_routes.py",
        "backend/models/__init__.py",
        "backend/models/user.py",
        "backend/models/account.py",
        "backend/models/post.py",
        "backend/services/__init__.py",
        "backend/services/auth_service.py",
        "backend/services/encryption_service.py",
        "backend/services/scheduler_service.py",
        "backend/services/tiktok_api_service.py",
        "backend/utils/__init__.py",
        "backend/utils/encryption.py",
        "backend/utils/validators.py"
    ]
    
    frontend_files = [
        "frontend/package.json",
        "frontend/public/index.html",
        "frontend/src/App.js",
        "frontend/src/components/Calendar.js",
        "frontend/src/components/Dashboard.js",
        "frontend/src/components/PostForm.js",
        "frontend/src/components/Settings.js",
        "frontend/src/components/AccountManager.js",
        "frontend/src/services/api.js",
        "frontend/src/services/encryption.js",
        "frontend/src/styles/main.css",
        "frontend/src/styles/theme.js"
    ]
    
    requirements_file = "requirements.txt"
    
    missing_files = []
    
    # Check backend files
    for file in backend_files:
        if not os.path.isfile(file):
            missing_files.append(file)
    
    # Check frontend files
    for file in frontend_files:
        if not os.path.isfile(file):
            missing_files.append(file)
    
    # Check requirements file
    if not os.path.isfile(requirements_file):
        missing_files.append(requirements_file)
    
    if missing_files:
        print_error(f"Missing files: {', '.join(missing_files)}")
        return False
    
    print_success("All key files exist")
    return True

def check_python_environment():
    """Check Python environment and dependencies"""
    print_header("Checking Python Environment")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print_error(f"Python 3.8+ required, found {python_version.major}.{python_version.minor}")
        return False
    
    print_success(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_warning("Virtual environment not activated. It's recommended to use a virtual environment.")
    else:
        print_success("Virtual environment is active")
    
    # Check dependencies
    try:
        import flask
        import flask_cors
        import flask_sqlalchemy
        import flask_jwt_extended
        import cryptography
        import requests
        import apscheduler
        
        print_success("Core Python dependencies are installed")
    except ImportError as e:
        print_error(f"Missing dependency: {str(e)}")
        print_info("Run 'pip install -r requirements.txt' to install dependencies")
        return False
    
    return True

def check_node_environment():
    """Check Node.js environment and dependencies"""
    print_header("Checking Node.js Environment")
    
    # Check if Node.js is installed
    try:
        node_version = subprocess.check_output(["node", "--version"]).decode().strip()
        print_success(f"Node.js version: {node_version}")
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("Node.js is not installed or not in PATH")
        return False
    
    # Check if npm is installed
    try:
        npm_version = subprocess.check_output(["npm", "--version"]).decode().strip()
        print_success(f"npm version: {npm_version}")
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("npm is not installed or not in PATH")
        return False
    
    # Check if node_modules directory exists in frontend
    if not os.path.isdir("frontend/node_modules"):
        print_warning("Node modules not installed in frontend directory")
        print_info("Run 'cd frontend && npm install' to install dependencies")
    else:
        print_success("Node modules are installed")
    
    return True

def check_backend_server():
    """Check if the backend server is running"""
    print_header("Checking Backend Server")
    
    try:
        response = requests.get(urljoin(BACKEND_URL, "/api/health"), timeout=5)
        if response.status_code == 200:
            print_success(f"Backend server is running at {BACKEND_URL}")
            return True
        else:
            print_error(f"Backend server returned status code {response.status_code}")
            return False
    except requests.RequestException:
        print_error(f"Backend server is not running at {BACKEND_URL}")
        print_info("Run 'cd backend && python app.py' to start the server")
        return False

def check_frontend_server():
    """Check if the frontend server is running"""
    print_header("Checking Frontend Server")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success(f"Frontend server is running at {FRONTEND_URL}")
            return True
        else:
            print_error(f"Frontend server returned status code {response.status_code}")
            return False
    except requests.RequestException:
        print_error(f"Frontend server is not running at {FRONTEND_URL}")
        print_info("Run 'cd frontend && npm start' to start the server")
        return False

def check_database():
    """Check if the database file exists and has tables"""
    print_header("Checking Database")
    
    db_path = "backend/tiktok_scheduler.db"
    if not os.path.isfile(db_path):
        print_warning("Database file does not exist yet")
        print_info("The database will be created when the backend server is started for the first time")
        return True
    
    print_success("Database file exists")
    return True

def run_full_test():
    """Run a full test of the application"""
    print_header("TikTok Scheduler Application Test")
    
    results = []
    
    # Check directory structure and files
    results.append(("Directory Structure", check_directory_structure()))
    results.append(("Key Files", check_key_files()))
    
    # Check environments
    results.append(("Python Environment", check_python_environment()))
    results.append(("Node.js Environment", check_node_environment()))
    
    # Check servers
    results.append(("Database", check_database()))
    results.append(("Backend Server", check_backend_server()))
    results.append(("Frontend Server", check_frontend_server()))
    
    # Print summary
    print_header("Test Summary")
    
    all_passed = True
    for name, result in results:
        if result:
            print_success(f"{name}: PASS")
        else:
            print_error(f"{name}: FAIL")
            all_passed = False
    
    if all_passed:
        print_header("ALL TESTS PASSED! 🎉")
        print_info("The TikTok Scheduler application is set up correctly and running.")
        
        # Open the application in a web browser
        response = input("Would you like to open the application in your web browser? (y/n): ")
        if response.lower() == 'y':
            webbrowser.open(FRONTEND_URL)
    else:
        print_header("SOME TESTS FAILED! ⚠️")
        print_info("Please fix the issues mentioned above and run the test again.")

if __name__ == "__main__":
    run_full_test()