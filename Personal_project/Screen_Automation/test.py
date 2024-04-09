import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from appium.webdriver.webdriver import AppiumOptions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define desired capabilities
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['browserName'] = 'brave'
capabilities['version'] = 'latest'
capabilities['platform'] = 'Windows 10'
#capabilities['chromeOptions'] = {'args': []}


# Initialize AppiumOptions and load your capabilities
appium_options = AppiumOptions()
appium_options.load_capabilities(capabilities)

# Connect to the existing browser session with options
driver = webdriver.Remote(
    command_executor="http://localhost:9222",
    options=appium_options
)

# Navigate to TikTok
# my_address = "https://www.tiktok.com/login/phone-or-email/email"
# driver.get(my_address)

print('Opened TikTok sign-in page')