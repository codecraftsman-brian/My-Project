from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent

client: TikTokLiveClient = TikTokLiveClient(
    unique_id="@caroondire"
)

# Shows the room id
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print("connected to the Room Id: ", client.room_id)

# Define the event handler function for comment events
@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    print(f"{event.user.unique_id} -> {event.comment}")

# @client.on(GiftEvent)
# async def on_gift(event: GiftEvent):
#     print(f"{event.user.unique_id} sent a {event.gift.gift_id}!")
#     for giftInfo in client.available_gifts:
#         if giftInfo["id"] == event.gift.gift_id:
#             print(f"Name: {giftInfo['name']} image: {giftInfo['image']['url_list'][0]} Diamond Amount: {giftInfo['diamond_count']}")

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    print(f"{event.user.unique_id} has liked this video {event.count} times, there is now {event.total} total likes.")

@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    print(f"{event.user.unique_id} followed the streamer!")

@client.on(ShareEvent)
async def on_share(event: ShareEvent):
    print(f"{event.user.unique_id} has shared a video!")

if __name__ == "__main__":
    client.run()