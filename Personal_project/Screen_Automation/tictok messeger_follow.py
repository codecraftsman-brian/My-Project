import pyautogui
import time
import random

click_interval = 0

def tiktok_icon():
    tiktok=((1048,1049),(89,24))
    for tic in tiktok:
        pyautogui.moveTo(tic[0], tic[1], duration=2)
        pyautogui.click()
        time.sleep(2)
    time.sleep(click_interval)
    follow_tiktok(8)
    # send_message(2)

def follow_tiktok(max_iterations=None):
    iteration_count = 0
    follow_tab=((42,684),(877,253),(1247,229))
    for tic in follow_tab:
        pyautogui.moveTo(tic[0], tic[1], duration=2)
        pyautogui.click()
        time.sleep(2)
    while max_iterations is None or iteration_count < max_iterations:
        x = 1196
        for y in range(300, 1000, 100):
            pyautogui.moveTo(x, y, duration=1)
            pyautogui.click()
        
        # Scroll up 6 button positions (6 * 100px = 600px)
        pyautogui.scroll(-675)  
        time.sleep(2)
        
        iteration_count += 1

def send_message(max_iterations=None):
    iteration_count = 0 
    pyautogui.moveTo(126,572, duration=2)
    pyautogui.click()
    pyautogui.click() #double clicks on the message tab
    time.sleep(10)
    while max_iterations is None or iteration_count < max_iterations:
        x = 451  # x coordinate for names
        start_y = 362  # starting y coordinate for first name
        
        for i in range(7):  # 7 names total
            # Calculate y coordinate for each name (decreasing by 100 each time)
            name_y = start_y + (i * 95)
            
            # Click on the name
            pyautogui.moveTo(x, name_y, duration=2)
            pyautogui.click()
            time.sleep(1)
            
            # Move to input field and paste message
            pyautogui.moveTo(1121, 967, duration=1)
            pyautogui.click()
            time.sleep(0.5)
            
            # Paste message
            pyautogui.hotkey('ctrl', 'v')  # Make sure message is in clipboard first
            # OR type directly: pyautogui.write(message)
            time.sleep(0.5)
            
            #Send
            pyautogui.press('enter')
            time.sleep(1)
        
        # Scroll down after completing all 7 clicks
        pyautogui.moveTo(286, 521, duration=1)
        pyautogui.scroll(-605)  # Positive value scrolls down
        time.sleep(1)
        
        iteration_count += 1

def insta_icon():
    # Initial click to the instagram tab
    pyautogui.moveTo(987, 1052, duration=1)
    pyautogui.click()
    time.sleep(2)
    # Refresh the page
    pyautogui.hotkey('ctrl','r')
    time.sleep(5)
    # Home click 
    pyautogui.moveTo(128, 200, duration=1)
    pyautogui.click()
    time.sleep(2)
    
    # Navigate to see All
    pyautogui.moveTo(1696, 187, duration=1)
    pyautogui.click()
    time.sleep(3)
    pyautogui.moveTo(1405, 214, duration=1)
    # pyautogui.click()
    time.sleep(1)
    
    for cycle in range(2):  # Run the whole process twice
        # Loop through the process 3 times
        base_x, base_y = 1405, 214
        for round_num in range(3):
            # Click 10 buttons with y increment of 85
            for i in range(10):
                y_position = base_y + (i * 85)
                pyautogui.moveTo(base_x,y_position, duration=1)
                pyautogui.click()
                time.sleep(1)  # Small delay between clicks, adjust as needed
            base_y = 214

            # Scroll up to reset position for next round (except on last round)
            if round_num < 2:  # Don't scroll after the last round
                total_scroll = 10 * -79  # Total distance to scroll
                scroll_steps = 20  # Number of steps to divide the scroll into
                scroll_per_step = total_scroll // scroll_steps
                delay_between_steps = 0.05  # 50ms delay between each step
                
                for _ in range(scroll_steps):
                    pyautogui.scroll(scroll_per_step)
                    time.sleep(delay_between_steps)
                time.sleep(2)  # Final pause
        
        # Refresh page after completing 3 rounds (except after the final cycle)
        if cycle < 1: 
            pyautogui.hotkey('ctrl', 'r')
            time.sleep(8)  # Wait for page to reload

# while True:
# tiktok_icon()
insta_icon() 
