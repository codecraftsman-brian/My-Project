import random

cards = [11,2,3,4,5,6,7,8,9,10,10,10]
#cards = random.choice(cards)
user_cards = random.sample(cards,2)
Computer_cards = random.sample(cards,2)
user_total = sum(user_cards)
computer_total = sum(Computer_cards)
print(f"--------------------{Computer_cards}")
print(f"computer's 1st card is: {Computer_cards[0]}")
print(f"Your cards are {user_cards}")

# if computer_total == 21:
#     print("Computer Wins!!")
# elif user_total == 21:
#     print("User Wins!!")
# elif computer_total == 21 and user_total == 21:
#     print("It's a Draw")

add_card = input("Do you want to get another card?")

if add_card == 'y':
    another_card = random.choice(cards)
    user_cards.append(another_card)
    if user_total > 21:
        print("YOU LOSE!! Game is over")
    elif user_total > computer_total and user_total <= 21:
        print(f" one {user_total}")
        print(f" one {computer_total}")
        print("User has won the game!")
    elif computer_total > user_total and computer_total <= 21: 
        print(f" two {user_total}")
        print(f" two {computer_total}")
        print("Computer has won the game!")
else:
    if user_total > computer_total and user_total <= 21:
        print(f" three {user_total}")
        print(f" three {computer_total}")
        print("User has won the game!")
    elif computer_total > user_total and computer_total <= 21:
        print(f" four {user_total}")
        print(f" four {computer_total}") 
        print("Computer has won the game!")

