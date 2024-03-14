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

# Open Chrome
my_path= "F:\Chrome\chromedriver-win64/chromedriver.exe"
chrome_service = Service(my_path)
driver = webdriver.Chrome(service=chrome_service)
logging.info('Chrome Opened Successfully')

# Navigate to TikTok
my_address = "https://www.tiktok.com/login"
driver.get(my_address)

logging.info('Opened tictok page')

time.sleep(500)
# Wait for the page to load and the Sign-In buttons to be clickable
wait = WebDriverWait(driver, 20)
google_sign_in_button_XPath = '//div[text() = "Use phone / email / username"]'
google_sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, google_sign_in_button_XPath)))
google_sign_in_button.click()

logging.info("clicked on google sign in")
# Switch to the pop-up window
# Note: This assumes the pop-up is the only window opened after the click. If there are multiple windows, you might need to adjust this.
driver.switch_to.window(driver.window_handles[-1])

wait = WebDriverWait(driver, 20)
use_email_XPath = '//a[@href="/login/phone-or-email/email"]'
use_email = wait.until(EC.element_to_be_clickable((By.XPATH, use_email_XPath)))
use_email.click()

print('clicked on use email')

# Locate the email input field and input your email address
email_log_in_XPath = '//input[@placeholder = "Email or username"]'
email_log_in = wait.until(EC.element_to_be_clickable((By.XPATH, email_log_in_XPath)))
email_log_in.click()

print('email input activated')
# Locate the email input field and input your email address
my_email = 'belisamelia17@gmail.com'
input_email_xpath = '//input[@placeholder = "Email or username"]'
input_email = driver.find_element(By.XPATH, input_email_xpath)
input_email.send_keys(my_email) 

print('Email inputted')

# Locate the password input field and input your password
my_password = 'karis@24'
input_password_xpath = '//input[@placeholder = "Password"]'
input_password = driver.find_element(By.XPATH, input_password_xpath)
input_password.send_keys(my_password)

print('password inputted')
#Locate the sign-in button and click it
sign_in_xpath = '//*[@id="loginContainer"]/div[2]/form/button'
sign_in_button = driver.find_element(By.XPATH, sign_in_xpath)
sign_in_button.click()

print("Have you bypassed the CAPTCHA authentication? (Press Enter to continue if yes):")

# Wait for the user to press Enter
input()

# If the user presses Enter, continue running the code
print("Continuing with the code...")

# Wait for a bit to ensure the page has time to load or any other necessary actions
time.sleep(300)
