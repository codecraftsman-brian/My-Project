#!/usr/bin/env python3
"""
Test runner script for the Telegram Message Scheduler.
This script runs all tests and produces a summary report.
"""

import sys
import os
import time
import subprocess
from datetime import datetime

def print_header(text):
    """Print a header with uniform formatting."""
    print("\n" + "=" * 70)
    print(f" {text} ".center(70, "="))
    print("=" * 70 + "\n")

def run_test_script(script_name, script_path):
    """Run a test script and return the result."""
    print_header(f"Running {script_name}")
    
    start_time = time.time()
    process = subprocess.run(
        [sys.executable, script_path], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    end_time = time.time()
    
    print(process.stdout)
    
    if process.stderr:
        print("Errors:")
        print(process.stderr)
    
    return {
        "name": script_name,
        "success": process.returncode == 0,
        "duration": end_time - start_time,
        "output": process.stdout,
        "error": process.stderr
    }

def run_validation_tests():
    """Run server validation tests without starting the server."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_scripts = [
        ("Environment Tests", os.path.join(test_dir, "tests", "test_environment.py")),
    ]
    
    results = []
    for script_name, script_path in test_scripts:
        results.append(run_test_script(script_name, script_path))
    
    return results

def run_unit_tests():
    """Run unit tests for the application."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_scripts = [
        ("Scheduler Tests", os.path.join(test_dir, "tests", "test_scheduler.py")),
        ("Web Interface Tests", os.path.join(test_dir, "tests", "test_web.py")),
    ]
    
    results = []
    for script_name, script_path in test_scripts:
        results.append(run_test_script(script_name, script_path))
    
    return results

def print_summary(results):
    """Print a summary of test results."""
    print_header("Test Results Summary")
    
    all_passed = True
    for result in results:
        status = "[PASS]" if result["success"] else "[FAIL]"
        print(f"{result['name']}: {status} ({result['duration']:.2f} seconds)")
        all_passed = all_passed and result["success"]
    
    print("\n" + "-" * 70)
    if all_passed:
        print("All tests passed successfully! The application is ready for deployment.")
        print("\nNext steps:")
        print("1. Follow the installation guide to set up the application")
        print("2. Configure your Telegram API credentials")
        print("3. Add messages and targets")
        print("4. Start the scheduler")
    else:
        print("Some tests failed. Please fix the issues before proceeding.")
    
    return all_passed

def main():
    """Run all tests and print a summary."""
    print_header("Telegram Message Scheduler - Validation Tests")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This will run validation tests to ensure the application is ready for deployment.")
    
    validation_results = run_validation_tests()
    
    # Only run unit tests if environment tests pass
    unit_results = []
    if all(result["success"] for result in validation_results):
        unit_results = run_unit_tests()
    
    all_results = validation_results + unit_results
    success = print_summary(all_results)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())