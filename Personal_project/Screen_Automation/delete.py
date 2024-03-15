import pyautogui
import time
import random

screen_width, screen_height = pyautogui.size()

click_interval = 90

#Screen 1
teamviewers_a=1610
teamviewers_b=858

teamviewers_a1=531
teamviewers_b1=858

teamviewers_a2=528
teamviewers_b2=379

teamviewers_a3=1693
teamviewers_b3=379

while True:
    pyautogui.moveTo(teamviewers_a,teamviewers_b, duration=2)
    pyautogui.click()

    time.sleep(click_interval)

    pyautogui.moveTo(teamviewers_a1,teamviewers_b1, duration=2)
    pyautogui.click()

    time.sleep(click_interval)

    pyautogui.moveTo(teamviewers_a2,teamviewers_b2, duration=2)
    pyautogui.click()

    time.sleep(click_interval)

    pyautogui.moveTo(teamviewers_a3,teamviewers_b3, duration=2)
    pyautogui.click()
    time.sleep(click_interval)
#############

# #Screen 2
# teamviewers_a=2827
# teamviewers_b=196

# teamviewers_a1=2795
# teamviewers_b1=563

# teamviewers_a2=2076
# teamviewers_b2=197

# teamviewers_a3=2069
# teamviewers_b3=523

# while True:
#     pyautogui.moveTo(teamviewers_a,teamviewers_b, duration=2)
#     pyautogui.click()

#     time.sleep(click_interval)

#     pyautogui.moveTo(teamviewers_a1,teamviewers_b1, duration=2)
#     pyautogui.click()

#     time.sleep(click_interval)

#     pyautogui.moveTo(teamviewers_a2,teamviewers_b2, duration=2)
#     pyautogui.click()

#     time.sleep(click_interval)

#     pyautogui.moveTo(teamviewers_a3,teamviewers_b3, duration=2)
#     pyautogui.click()
#     time.sleep(click_interval)

# ##################
    
# import pygetwindow as gw

# # Define the title of the application window you want to check
# app_title = "Arthur Ngugi - TeamViewer"

# # Get the active (foreground) window
# active_window = gw.getActiveWindow()

# if active_window and active_window.title == app_title:
#     print(f"{app_title} is the foreground application.")
# else:
#     print(f"{app_title} is not the foreground application.")




# # Get the name of the window that is on the forebackground
# from pynput.mouse import Listener
# def is_open():
#     teamviewers=((0,255), (190,353))
#     for teamviewer in teamviewers:
#         pyautogui.moveTo(teamviewer[0], teamviewer[1], duration=2)
        
#     press = True
#     while press == True:
#         def click(x, y, button, pressed):
#             if pressed:
#                 window_under_cursor = gw.getWindowsAt(x, y)
#                 app_name = window_under_cursor[0].title
#                 if app_name == "Arthur Ngugi - TeamViewer":
#                     return "TeamView is open"
#                 else:
#                     return "Not open"
#         press = False

#     with Listener(on_click=click) as listener:
#         listener.join()
