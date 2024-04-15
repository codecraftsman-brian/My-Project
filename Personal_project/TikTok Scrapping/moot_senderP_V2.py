from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
import pyautogui
import time
import asyncio
import random

client: TikTokLiveClient = TikTokLiveClient(
    unique_id="@lizliz.malimar"
)

unique_ids = []
target_position =(1151,733, 1340,726)

# Define the event handler function for comment events
@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    # Add the unique ID to the set (automatically handles uniqueness)
    while event.user.unique_id not in unique_ids:
        time.sleep(1)
        # Pick the first user from the list
        unique_ids.append(event.user.unique_id)
        print("#######################################################################") 
        print(f"{event.user.unique_id} was appended in the list")
        print(unique_ids)
        print(f"{event.user.unique_id} -> {event.comment}")
        print(f"we have a total of {len(unique_ids)} commentor")
        print("#######################################################################") 
        time.sleep(1)

    # Process the comment asynchronously
    #asyncio.create_task(comment_activate(target_position, event.user.unique_id))
        item_index = 0
        list_length = 0
        if len(unique_ids) > list_length:
            time.sleep(1)
            print("*******************************************************************")
            print(f"the length of the list is: {len(unique_ids)}")
            print(f"Sending a comment to {unique_ids[item_index]}")
            time.sleep(1)
            print("*******************************************************************")
        item_index += 1
        list_length = len(unique_ids)



 

# async def comment_activate(position, message):
#     my_comment = ["Moot", "Mooot", "Moot Me"]
#     selected_moot = my_comment[random.randint(0,2)]
#     comment = f"@{message} {selected_moot} "
#     pyautogui.moveTo(position[0], position[1], duration=0.5)
#     pyautogui.click()
#     time.sleep(1)
#     pyautogui.typewrite(comment)
#     time.sleep(2)
#     pyautogui.moveTo(position[2], position[3], duration=1)
#     #pyautogui.click()      

if __name__ == "__main__":
    client.run()