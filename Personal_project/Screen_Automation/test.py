from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

# Command to start Chrome with a specific profile and remote debugging enabled
command = 'chrome.exe --profile-directory="Profile 5" --remote-debugging-port=9222'

# Run the command
subprocess.run(command, shell=True)

# Wait for Chrome to start (you can adjust the sleep duration based on your system)
time.sleep(5)

# Connect to the remote debugging port using Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Create a new WebDriver instance
driver = webdriver.Chrome(options=chrome_options)

# Navigate to a website (replace 'https://www.example.com' with the address you want to search)
driver.get('https://www.tiktok.com/')