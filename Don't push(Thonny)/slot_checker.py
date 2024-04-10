import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(r"--user-data-dir=C:\Users\Charis\AppData\Local\Google\Chrome\User Data") # Replace with your Chrome user data directory
chrome_options.add_argument(r'--profile-directory=Profile 1') # Replace with your Chrome profile directory
print('completed 1')
# Specify the path to chromedriver.exe
webdriver_service = Service('C:\Program Files\Google\Chrome\Application\chrome.exe')

print('completed 2')
# Open the website
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.get('https://ais.usvisa-info.com/en-ke/niv/groups/38768183')

print('completed 3')
# Your login credentials
username = 'briankariuki274@gmail.com'
password = '2022@Stop@@'

# Find username and password fields and enter your credentials
driver.find_element(By.ID, 'username').send_keys(username)
driver.find_element(By.ID, 'password').send_keys(password)

# Click the login button
driver.find_element(By.ID, 'login').click()

# Navigate to the booking page
driver.get('https://ais.usvisa-info.com/en-ke/niv/schedule/54605163/appointment')

# Parse the page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Get the current year
current_year = datetime.datetime.now().year

# Loop over the months from February to June
for month in range(2, 12):
    # Check if there are any available slots for the current month
    available_slots = soup.find_all('div', {'class': f'available-{month}-{current_year}'})
    if available_slots:
        print(f'Available slots for {month}/{current_year}')
        for slot in available_slots:
            print(slot.text)
    else:
        print(f'No available slots for {month}/{current_year}')

# Close the browser
driver.quit()