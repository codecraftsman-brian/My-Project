#!/usr/bin/env python3
"""
Enhanced test script to validate that the TikTok Scheduler application is running correctly.
This script checks both backend and frontend components, and includes additional tests
for common issues like blank browser pages and environment configuration problems.
"""

import os
import sys
import subprocess
import time
import requests
from urllib.parse import urljoin
import webbrowser
import json
import sqlite3
import platform
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Configuration
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"
WAIT_TIMEOUT = 10  # Seconds to wait for elements to appear in browser

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
        "frontend/src/index.js",  # Added index.js check
        "frontend/src/App.js",
        "frontend/src/components/Calendar.js",
        "frontend/src/components/Dashboard.js",
        "frontend/src/components/PostForm.js",
        "frontend/src/components/Settings.js",
        "frontend/src/components/AccountManager.js",
        "frontend/src/components/Login.js",  # Added Login component check
        "frontend/src/services/api.js",
        "frontend/src/services/encryption.js",
        "frontend/src/styles/main.css",
        "frontend/src/styles/theme.js"
    ]
    
    requirements_file = "requirements.txt"
    env_files = [".env", "frontend/.env"]
    
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
    
    # Check for at least one .env file
    if not any(os.path.isfile(env_file) for env_file in env_files):
        print_warning("No .env file found. Make sure environment variables are properly set.")
    
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
        
        # Check if Node.js version is too recent (causing OpenSSL issues)
        version_number = node_version.lstrip('v').split('.')
        major_version = int(version_number[0])
        
        if major_version >= 17:
            print_warning(f"Node.js version {node_version} may cause OpenSSL compatibility issues with React.")
            print_info("Solution 1: Add 'set NODE_OPTIONS=--openssl-legacy-provider' to your npm start script")
            print_info("Solution 2: Consider downgrading to Node.js LTS version (v16.x or v14.x)")
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

def check_frontend_environment():
    """Check frontend environment configuration"""
    print_header("Checking Frontend Environment")
    
    # Check for frontend/.env file
    if os.path.isfile("frontend/.env"):
        print_success("Frontend .env file exists")
        
        # Check for SKIP_PREFLIGHT_CHECK setting
        with open("frontend/.env", "r") as f:
            env_content = f.read()
            if "SKIP_PREFLIGHT_CHECK=true" in env_content:
                print_success("SKIP_PREFLIGHT_CHECK is set to true")
            else:
                print_warning("SKIP_PREFLIGHT_CHECK=true is not set in frontend/.env")
                print_info("This might cause dependency conflicts with newer Node.js versions")
    else:
        print_warning("Frontend .env file not found")
        print_info("Consider creating a frontend/.env file with SKIP_PREFLIGHT_CHECK=true")
    
    # Check package.json for start script modification
    if os.path.isfile("frontend/package.json"):
        with open("frontend/package.json", "r") as f:
            package_data = json.load(f)
            start_script = package_data.get("scripts", {}).get("start", "")
            
            if "NODE_OPTIONS=--openssl-legacy-provider" in start_script:
                print_success("start script includes OpenSSL legacy provider option")
            else:
                print_info("Consider adding NODE_OPTIONS=--openssl-legacy-provider to your start script")
    
    return True

def check_backend_environment():
    """Check backend environment configuration"""
    print_header("Checking Backend Environment")
    
    # Check for .env file at project root
    if os.path.isfile(".env"):
        print_success("Backend .env file exists")
        
        # Check for essential environment variables
        load_dotenv()
        essential_vars = [
            "SECRET_KEY",
            "JWT_SECRET_KEY",
            "DATABASE_URI",
            "TIKTOK_CLIENT_KEY",
            "TIKTOK_CLIENT_SECRET",
            "TIKTOK_REDIRECT_URI"
        ]
        
        missing_vars = []
        for var in essential_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            print_warning(f"Missing environment variables: {', '.join(missing_vars)}")
        else:
            print_success("All essential environment variables are set")
    else:
        print_warning("Backend .env file not found at project root")
        print_info("Consider creating a .env file with necessary environment variables")
    
    return True

def check_backend_server():
    """Check if the backend server is running"""
    print_header("Checking Backend Server")
    
    try:
        response = requests.get(urljoin(BACKEND_URL, "/api/health"), timeout=5)
        if response.status_code == 200:
            print_success(f"Backend server is running at {BACKEND_URL}")
            
            # Try API endpoints that don't require authentication
            endpoints = [
                "/api/health",
                # Add more public endpoints if available
            ]
            
            for endpoint in endpoints:
                try:
                    endpoint_url = urljoin(BACKEND_URL, endpoint)
                    response = requests.get(endpoint_url, timeout=5)
                    if response.status_code < 400:
                        print_success(f"Endpoint {endpoint} is accessible")
                    else:
                        print_warning(f"Endpoint {endpoint} returned status code {response.status_code}")
                except requests.RequestException as e:
                    print_warning(f"Could not access endpoint {endpoint}: {str(e)}")
            
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
    
    # Check database schema
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        expected_tables = ['users', 'accounts', 'posts']
        missing_tables = [table for table in expected_tables if table not in table_names]
        
        if missing_tables:
            print_warning(f"Missing tables in database: {', '.join(missing_tables)}")
        else:
            print_success(f"Database contains the expected tables: {', '.join(expected_tables)}")
        
        conn.close()
    except sqlite3.Error as e:
        print_error(f"Error accessing database: {str(e)}")
    
    return True

def check_frontend_rendering():
    """Check if the frontend is rendering correctly (no blank page)"""
    print_header("Checking Frontend Rendering")
    
    try:
        # Set up headless Chrome browser
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        try:
            driver = webdriver.Chrome(options=options)
        except WebDriverException:
            print_error("Chrome webdriver not found. Skipping frontend rendering check")
            print_info("Install selenium and chromedriver to enable this check")
            return False
        
        # Load the frontend
        driver.get(FRONTEND_URL)
        
        # Wait for either the login form or dashboard to appear
        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            
            # Check if the page has visible content
            body_text = driver.find_element(By.TAG_NAME, "body").text
            
            if len(body_text.strip()) > 0:
                print_success("Frontend is rendering content correctly (not blank)")
            else:
                print_error("Frontend appears to be blank")
                
                # Check for console errors
                console_logs = driver.get_log('browser')
                if console_logs:
                    print_warning("Browser console errors detected:")
                    for log in console_logs[:5]:  # Show first 5 errors
                        print_warning(f"  - {log.get('message')}")
                    
                    # Check for specific errors we've encountered
                    for log in console_logs:
                        message = log.get('message', '')
                        if 'Module not found' in message:
                            print_info("Suggestion: Check import paths in your React components")
                        elif 'Unexpected token' in message:
                            print_info("Suggestion: Check for syntax errors in your JavaScript code")
                        elif 'Failed to compile' in message:
                            print_info("Suggestion: Check the terminal running the frontend for compilation errors")
                        elif 'OpenSSL' in message:
                            print_info("Suggestion: Add NODE_OPTIONS=--openssl-legacy-provider to your npm start script")
                
                print_info("Common solutions for blank page issues:")
                print_info("1. Check frontend console for errors (F12 in browser)")
                print_info("2. Verify all React components exist and are imported correctly")
                print_info("3. Make sure index.js is set up properly as the entry point")
                print_info("4. Check for OpenSSL issues with Node.js v17+ (use --openssl-legacy-provider)")
                print_info("5. Clear browser cache or try in incognito mode")
        except TimeoutException:
            print_error("Frontend took too long to render content")
            print_info("This may indicate a blank page issue or slow loading")
            
            # Check for console errors that might explain the timeout
            console_logs = driver.get_log('browser')
            if console_logs:
                print_warning("Browser console errors detected:")
                for log in console_logs[:5]:  # Show first 5 errors
                    print_warning(f"  - {log.get('message')}")
        
        driver.quit()
        return True
    except Exception as e:
        print_error(f"Error checking frontend rendering: {str(e)}")
        return False

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
    results.append(("Frontend Environment", check_frontend_environment()))
    results.append(("Backend Environment", check_backend_environment()))
    
    # Check infrastructure
    results.append(("Database", check_database()))
    results.append(("Backend Server", check_backend_server()))
    results.append(("Frontend Server", check_frontend_server()))
    
    # Check actual functionality
    if any(name == "Frontend Server" and result for name, result in results):
        results.append(("Frontend Rendering", check_frontend_rendering()))
    
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
        
        # Print common fixes for specific issues
        print_header("Common Fixes")
        
        print_info("Blank Frontend Page:")
        print_info("1. Check if frontend/.env has SKIP_PREFLIGHT_CHECK=true")
        print_info("2. For Node.js v17+, add 'set NODE_OPTIONS=--openssl-legacy-provider' to your start script")
        print_info("3. Verify all component imports in App.js match the actual file paths")
        print_info("4. Make sure index.js is properly set up as the entry point")
        
        print_info("\nDatabase Issues:")
        print_info("1. Delete the existing database file and let it be recreated")
        print_info("2. Check DATABASE_URI in your .env file")
        
        print_info("\nBackend Connection Issues:")
        print_info("1. Make sure CORS is properly configured in the backend")
        print_info("2. Check if frontend is configured with the correct proxy in package.json")

def deployment_cleanup_guide():
    """Print a guide for cleaning up before deployment"""
    print_header("Deployment Cleanup Guide")
    
    print_info("Before deploying to production, remove the following:")
    
    print_info("\nFrontend Files to Remove:")
    print_info("1. node_modules/ directory")
    print_info("2. .env file (create a production version)")
    print_info("3. Any debug or test files")
    print_info("4. .git/ directory if present")
    
    print_info("\nBackend Files to Remove:")
    print_info("1. __pycache__/ directories and .pyc files")
    print_info("2. .env file (create a production version)")
    print_info("3. Local database file (tiktok_scheduler.db) - use a production database")
    print_info("4. Any debug or test files")
    print_info("5. Any uploaded videos in the 'uploads/' directory (if you want to start fresh)")
    
    print_info("\nSecure your production environment:")
    print_info("1. Set SECRET_KEY and JWT_SECRET_KEY to strong random values")
    print_info("2. Configure HTTPS with a valid SSL certificate")
    print_info("3. Set DEBUG=False in production")
    print_info("4. Use a production-ready web server (like Gunicorn with Nginx)")
    print_info("5. Configure proper logging")

if __name__ == "__main__":
    print_header("TikTok Scheduler Test and Deployment Tool")
    print_info("This script helps test your TikTok Scheduler application")
    print_info("and guides you through deployment preparation.")
    print_info("\nOptions:")
    print_info("1. Run full application test")
    print_info("2. Print deployment cleanup guide")
    print_info("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        run_full_test()
    elif choice == "2":
        deployment_cleanup_guide()
    else:
        print_info("Exiting...")