import pyautogui
import time
import random
    # Set the target position where you want to click
target_position = (1600, 1039, 1886, 1037)

def send_message(message, position):
    pyautogui.moveTo(position[0], position[1], duration=2)
    pyautogui.click()
    pyautogui.typewrite(message)
    pyautogui.moveTo(position[2], position[3], duration=0.5)
    pyautogui.click()

while True:
    message_to_send = ["Moot","Moot me I moot back", "Moooot", "Moot for Moot", "Moot 4 Moot", "Mooooooot"]
    random_string = random.choice(message_to_send)
    send_message(random_string, target_position)

    # Wait for 5 seconds before the next iteration
    time.sleep(3)
