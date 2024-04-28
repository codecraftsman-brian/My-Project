import random
from art import logo

print(logo)
print("Welcome to this Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

guessed_number = random.randint(1,100)

def play_game():
    """This function checks whether the input from the user matches the computer guess"""
    attempts = 0
    game_level = input("Choose a difficulty. Type 'easy' or 'hard': ")
    if game_level == 'easy':
        attempts = 10
    elif game_level == 'hard':
        attempts = 5
    else:
        print("Incorrect value!")

    while attempts > 0:
        print(f"You have {attempts} attempts remaining to guess the number.")
        my_guess = int(input("Make a guess: "))
        if guessed_number < my_guess:
            print("Guess too high. Try again.")
        elif guessed_number > my_guess:
            print("Guess too low. Try again.")
            print("Guess again")
        elif guessed_number == my_guess:
            print(f"You got it! The answer was {guessed_number}")
            break
        attempts -= 1

        if attempts == 0:
            print("You've run out of guesses, you lose")
    
play_game()