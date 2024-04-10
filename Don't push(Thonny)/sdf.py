import pyautogui
import time
import random

click_interval = 2
scroll_wait_time = 1

def teamviewer():
    teamviewers=((0,255), (190,353))
    for teamviewer in teamviewers:
        pyautogui.moveTo(teamviewer[0], teamviewer[1], duration=2)
        pyautogui.click()
        
    time.sleep(click_interval)
    

teamviewer_is_open = 0

if teamviewer_is_open == 0:
    teamviewer()
    teamviewer_is_open += 1