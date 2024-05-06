import random
import os
print("Welcome to the BlackJack Capstone Game!")
user_name = input("What's your name? \n")
cards = [11,2,3,4,5,6,7,8,9,10,10,10]

play_again = True
while play_again:
    user_cards = random.sample(cards,2)
    computer_cards = random.sample(cards,2)

    print(f"computer's 1st card is: {computer_cards}")
    print(f"{user_name}, your cards are {user_cards}")

    sum_user_cards = sum(user_cards)
    sum_computer_cards = sum(computer_cards)

    if sum_user_cards > 21:
        print("Game is Over! You lost.")

    extra_card = True
    new_users_cards = user_cards
    new_comp_cards = computer_cards

    if computer_cards in [[10, 11],[11, 10]]:
        print(f"{user_name}, You Lost! ")
        extra_card = False
    elif user_cards in [[10, 11],[11, 10]]:
        print(f"{user_name}, You Won! ")
        extra_card = False

    while extra_card:
        add_extra_card = input("Do you want to get another card?")

        while sum(new_comp_cards) < 16:
            another_comp_card = random.choice(cards)
            new_comp_cards.append(another_comp_card) 
        if add_extra_card in ['y', 'Y', 'Yes','yes']:
            another_user_card = random.choice(cards)
            new_users_cards.append(another_user_card)
        else:
            extra_card = False

        print(f"computer's 1st card is: {new_comp_cards}")
        print(f"user_name, your cards are {new_users_cards}")

    if sum(new_users_cards) > sum(new_comp_cards) and sum(new_users_cards) <= 21:
        print(f"The total users sum is {sum(new_users_cards)} and the computers sum is {sum(new_comp_cards)}")
        print(f"{user_name} you have won the game!")
    elif sum(new_comp_cards) > sum(new_users_cards) and sum(new_comp_cards) <= 21:
        print(f"The total users sum is {sum(new_users_cards)} and the computers sum is {sum(new_comp_cards)}") 
        print("Computer has won the game!")
    elif sum(new_users_cards) == sum(new_comp_cards) and sum(new_comp_cards) <= 21:
        print(f"The total users sum is {sum(new_users_cards)} and the computers sum is {sum(new_comp_cards)}")
        print("You Draw! Try again")
    elif sum(new_comp_cards) <= 21 and sum(new_users_cards) >=21:
        print(f"The total users sum is {sum(new_users_cards)} and the computers sum is {sum(new_comp_cards)}")
        print("Computer has won the game!")
    elif sum(new_comp_cards) >= 21 and sum(new_users_cards) <=21:
        print(f"The total users sum is {sum(new_users_cards)} and the computers sum is {sum(new_comp_cards)}")
        print(f"{user_name} you have won the game!")
    else:
        print('CAUTION!!')
        print(f"The total users sum is {sum(new_users_cards)} and the computers sum is {sum(new_comp_cards)}")
    play_again = False
    restart_game = input(f"{user_name}, do you want to restart the game? ")
    
    if restart_game in ['y', 'Y', 'Yes','yes']:
        os.system('cls')
        play_again = True
    else:
        print(f"Goodbye {user_name}! The game has ended.")