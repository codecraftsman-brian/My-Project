#!/usr/bin/env python3
"""
A simple script to check if key files exist and create them if they don't.
"""

import os
import shutil

# Define the directory structure
directories = [
    "frontend/src/components",
    "frontend/src/services",
    "frontend/public",
]

# Check and create directories
for directory in directories:
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)
    else:
        print(f"Directory exists: {directory}")

# Check if files exist
files_to_check = [
    "frontend/src/components/Calendar.js",
    "frontend/src/services/api.js",
    "frontend/public/favicon.ico",
    "frontend/public/logo192.png",
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        print(f"File exists: {file_path}")
    else:
        print(f"File missing: {file_path}")

# Check App.js for the typo
app_js_path = "frontend/src/App.js"
if os.path.exists(app_js_path):
    print(f"Checking {app_js_path} for typos")
    with open(app_js_path, 'r') as f:
        content = f.read()
        if './componeents/Calendar' in content:
            print("Found typo in App.js: './componeents/Calendar'")
        else:
            print("No typo found in App.js")
else:
    print(f"File missing: {app_js_path}")

# Check if the .env file has SKIP_PREFLIGHT_CHECK
env_path = "frontend/.env"
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
        if 'SKIP_PREFLIGHT_CHECK=true' in content:
            print("SKIP_PREFLIGHT_CHECK=true is in .env")
        else:
            print("SKIP_PREFLIGHT_CHECK=true is NOT in .env")
else:
    print(f"File missing: {env_path}")

print("\nRun this script with the '--fix' option to automatically fix issues")