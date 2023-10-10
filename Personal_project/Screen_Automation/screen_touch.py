import pyautogui
import time
import random
# Define the screen dimensions (change these values based on your screen resolution)
screen_width, screen_height = pyautogui.size()

click_interval = 2
scroll_wait_time = 1

def teamviewer():
    teamviewers=((0,255), (190,353))
    for teamviewer in teamviewers:
        pyautogui.moveTo(teamviewer[0], teamviewer[1], duration=2)
        pyautogui.click()
        
    time.sleep(click_interval)

def folder():
    folders=((0,255), (190,353), (630, 1062), (613, 979),(1739, 103), (1087, 112))
    for folder in folders:
        pyautogui.moveTo(folder[0], folder[1], duration=2)
        pyautogui.click()
        
        time.sleep(click_interval)

def scroll_down():
    scroll_direction = -1  # 1 for scrolling up, -1 for scrolling down
    scroll_steps = 0  # You can adjust this number as needed

    while scroll_steps < 100:
        pyautogui.scroll(scroll_direction * scroll_steps)
        time.sleep(scroll_wait_time)
        scroll_steps +=1    

def scroll_up():
    scroll_direction = 1  # 1 for scrolling up, -1 for scrolling down
    scroll_steps = 0  # You can adjust this number as needed

    while scroll_steps < 20:
        pyautogui.scroll(scroll_direction * scroll_steps)
        time.sleep(scroll_wait_time)
        scroll_steps +=1 

def email():
    emails=((762,1056), (275,270))
    for email in emails:
        pyautogui.moveTo(email[0], email[1], duration=1)
        pyautogui.click()
        
        time.sleep(click_interval)

    scroll_up()
teamviewer_is_open = False
while True:
    # x = random.randint(0, screen_width)
    # y = random.randint(0, screen_height)

    while teamviewer_is_open == False:
        teamviewer()
        teamviewer_is_open = True
    folder()
    email()









    # folders=((17,445), (188,560), (630, 1062), (613, 979),(1739, 103), (1087, 112))
    # for folder in folders:
    #     pyautogui.moveTo(folder[0], folder[1], duration=2)
    #     pyautogui.click()

    #     scroll_direction = -1  # 1 for scrolling up, -1 for scrolling down
    #     scroll_steps = 0  # You can adjust this number as needed

    #     while scroll_steps < 10:
    #         pyautogui.scroll(scroll_direction * scroll_steps)
    #         #time.sleep(scroll_wait_time)
    #         scroll_steps +=1
    #         print(scroll_steps)
        
    #     time.sleep(click_interval)




   