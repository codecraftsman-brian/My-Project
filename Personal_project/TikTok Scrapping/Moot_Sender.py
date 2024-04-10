from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
import pyautogui
import time

#target_position =(2335,1400,2487,1400) #gold__ita, Lady.Kay_, kingangi_official
target_position =(1662,1042,1851,1047)
unique_ids = []

def comment_activate(position, message):
    pyautogui.moveTo(position[0], position[1], duration=0.5)
    pyautogui.click()
    time.sleep(1)
    comment = f"@{message} Mooot"
    pyautogui.typewrite(comment)
    time.sleep(2)
    pyautogui.moveTo(position[2], position[3], duration=1)
    pyautogui.click()

def run_client():
    client = TikTokLiveClient(unique_id="@gold__ita")
    
    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        print(f"{event.user.unique_id}")
        unique_ids.append(event.user.unique_id)
        comment_activate(target_position, event.user.unique_id)
        print(len(unique_ids))
    
    client.run()

def navigate_and_scroll():
    # pyautogui.moveTo(1074,468, duration=0.5)
    # pyautogui.click()
    # Navigate to a specific point
    pyautogui.moveTo(2444, 1250, duration=0.5)
    # Perform scrolling twice
    for _ in range(2):
        pyautogui.scroll(10)
        time.sleep(0.5)

if __name__ == "__main__":
    while True:
        try:
            run_client()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Performing navigation and scrolling before retrying...")
            navigate_and_scroll()
            time.sleep(10)  # Wait for a while before retrying