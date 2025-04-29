"""
Test the environment setup for the Telegram Message Scheduler.
This validates that all required packages are installed and accessible.
"""

import importlib
import sys
import os
import platform

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

def test_python_version():
    """Test that Python version is 3.7 or higher."""
    version_info = sys.version_info
    print(f"Python version: {sys.version}")
    assert version_info.major == 3 and version_info.minor >= 7, "Python 3.7+ is required"
    return True

def test_required_packages():
    """Test that all required packages are installed."""
    required_packages = {
        'flask': '2.0.0',
        'telethon': '1.24.0',
        'werkzeug': '2.0.0',
    }
    
    all_installed = True
    
    print("Checking required packages:")
    for package, min_version in required_packages.items():
        try:
            module = importlib.import_module(package)
            try:
                from importlib.metadata import version
                module_version = version(package)
            except ImportError:
                module_version = getattr(module, '__version__', 'unknown')
            print(f"  [PASS] {package} (version: {module_version})")
        except ImportError:
            print(f"  [FAIL] {package} is not installed")
            all_installed = False
    
    assert all_installed, "Not all required packages are installed"
    return all_installed

def test_directory_structure():
    """Test that the required directory structure exists."""
    required_dirs = [
        '',
        'scheduler',
        'web',
        'templates',
        'static',
        'static/js',
    ]
    
    all_dirs_exist = True
    
    print("Checking directory structure:")
    for directory in required_dirs:
        dir_path = os.path.join(parent_dir, directory)
        if os.path.isdir(dir_path):
            print(f"  [PASS] {directory or 'Project root'}")
        else:
            print(f"  [FAIL] {directory or 'Project root'} does not exist")
            all_dirs_exist = False
    
    assert all_dirs_exist, "Not all required directories exist"
    return all_dirs_exist

def test_required_files():
    """Test that all required files exist."""
    required_files = [
        'app.py',
        'config.py',
        'scheduler/__init__.py',
        'scheduler/models.py',
        'scheduler/utils.py',
        'web/__init__.py',
        'web/routes.py',
        'templates/base.html',
        'templates/index.html',
        'templates/setup.html',
        'static/js/main.js',
    ]
    
    all_files_exist = True
    
    print("Checking required files:")
    for file_path in required_files:
        full_path = os.path.join(parent_dir, file_path)
        if os.path.isfile(full_path):
            print(f"  [PASS] {file_path}")
        else:
            print(f"  [FAIL] {file_path} does not exist")
            all_files_exist = False
    
    assert all_files_exist, "Not all required files exist"
    return all_files_exist

def test_file_permissions():
    """Test that app.py is executable."""
    app_path = os.path.join(parent_dir, 'app.py')
    
    # Skip on Windows as executable bit doesn't apply
    if platform.system() == 'Windows':
        print("Skipping executable check on Windows")
        return True
    
    is_executable = os.access(app_path, os.X_OK)
    print(f"Checking if app.py is executable: {'Yes' if is_executable else 'No'}")
    
    if not is_executable:
        print("Warning: app.py is not executable. You may need to run 'chmod +x app.py'")
    
    return True  # Non-critical test

def run_all_tests():
    """Run all environment tests."""
    print("Running environment tests for Telegram Message Scheduler")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_required_packages,
        test_directory_structure,
        test_required_files,
        test_file_permissions,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except AssertionError as e:
            print(f"Test failed: {e}")
            results.append(False)
        except Exception as e:
            print(f"Error running test {test.__name__}: {e}")
            results.append(False)
        print("-" * 50)
    
    if all(results):
        print("All environment tests passed! [PASS]")
        return True
    else:
        print("Some tests failed. Please fix the issues before proceeding. [FAIL]")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)