from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
import pyautogui
import time
import asyncio
import random

client: TikTokLiveClient = TikTokLiveClient(
    unique_id= 'mwalimuwatiktok' #"@gold__ita"
)

# @client.on(ConnectEvent)
# async def on_connect(event: ConnectEvent):
#     client.logger.info(f"Connected to @{event.unique_id}!")

unique_ids = ['belisamelia']
target_position =(1129, 735, 1338, 731)

x = 1

@client.on(CommentEvent)
def on_comment(event: CommentEvent):
    while event.user.unique_id not in unique_ids:
        time.sleep(1)
        # Pick the first user from the list
        unique_ids.append(event.user.unique_id)
        print("#######################################################################") 
        print(f"{event.user.unique_id} was appended in the list")
        print(unique_ids)
        print(f"{event.user.unique_id} -> {event.comment}")
        print("#######################################################################") 
        time.sleep(1)

    on_send()

def on_send():
    global x
    if len(unique_ids) > x:
        my_comment = ["Moot", "Mooot", "Moot Me"]
        selected_moot = my_comment[random.randint(0,2)]
        comment = f"@{unique_ids[x]} {selected_moot} "
        print(comment)
        mouse_move(target_position, comment)
        time.sleep(1)
        x += 1
        print(f"Sent {x} comments") 

def mouse_move(hover_position,comment):
    pyautogui.moveTo(hover_position[0], hover_position[1], duration=0.5)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(comment)
    time.sleep(2)
    pyautogui.moveTo(hover_position[2], hover_position[3], duration=1)
    pyautogui.click() 



if __name__ == "__main__":
    while True:
        try:
            client.run()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Trying again...")
            time.sleep(10)