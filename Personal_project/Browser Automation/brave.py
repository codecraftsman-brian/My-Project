import time
import pyautogui
import logging
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to Brave browser executable
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# Path to ChromeDriver
driver_path = "F:/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Set up ChromeOptions to use Brave
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# Initialize WebDriver with Brave
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
logging.info('Brave Opened Successfully')

# Navigate to TikTok
my_address = "https://www.tiktok.com/login/phone-or-email/email"
driver.get(my_address)

print('Opened tictok sign in page')

# Wait for the page to load and the Sign-In buttons to be clickable
wait = WebDriverWait(driver, 20)
# Locate the email input field and input your email address
email_log_in_XPath = '//input[@placeholder="Email or username"]'
email_log_in = wait.until(EC.element_to_be_clickable((By.XPATH, email_log_in_XPath)))
email_log_in.click()

print('email input activated')
# Locate the email input field and input your email address
my_email = 'belisamelia17@gmail.com'
input_email_xpath = '//input[@placeholder="Email or username"]'
input_email = driver.find_element(By.XPATH, input_email_xpath)
input_email.send_keys(my_email) 

print('Email inputted')

# Locate the password input field and input your password
my_password = 'karis@24'
input_password_xpath = '//input[@placeholder="Password"]'
input_password = driver.find_element(By.XPATH, input_password_xpath)
input_password.send_keys(my_password)

print('password inputted')

#Locate the sign-in button and click it
sign_in_xpath = '//*[@id="loginContainer"]/div[1]/form/button'
sign_in_button = driver.find_element(By.XPATH, sign_in_xpath)
sign_in_button.click()

print('Login button clicked')

print("Have you bypassed the CAPTCHA authentication? (Press Enter to continue if yes):")

# Wait for the user to press Enter
input()

# If the user presses Enter, continue running the code
print("Continuing with the code...")

# Wait for a bit to ensure the page has time to load or any other necessary actions
time.sleep(300)
