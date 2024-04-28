from replit import clear
from art import logo

#HINT: You can call clear() to clear the output in the console.
print(logo)
print("welcome to the secret aution program.")


bidder_list = []

def bidder_func():
    bidder_dict = {}
    bidder_name = input("What is your name?: ")
    bidder_dict["name"] = bidder_name
    bid_price = input("What's your bid?: $")
    bidder_dict["bid"] = bid_price
    bidder_list.append(bidder_dict)

bidder_func()   
is_bidder = input("Are there any other bidders? Type 'yes' or 'no'.")

while is_bidder == 'yes':
    clear()
    bidder_func()
    is_bidder = input("Are there any other bidders? Type 'yes' or 'no'.")
    if int(bidder_list[0]["bid"]) > int(bidder_list[1]["bid"]):
        del bidder_list[1]
    else:
        del bidder_list[0]

print(f'The winner is {bidder_list[0]["name"]} with a bid of ${bidder_list[0]["bid"]}.')