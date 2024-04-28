import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

game_option = [rock, paper, scissors]

my_choice = int(input("What so you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors \n"))
if my_choice not in [0,1,2]:
    print("You typed an Invalid number, please try again.")
else:
    print(game_option[my_choice])

    print("Computer choice:")
    comp_choice = random.randint(0,2)
    print("Computer choosed: " + str(comp_choice))
    print(game_option[comp_choice])

    if (my_choice == 0 and comp_choice == 0) or (my_choice == 1 and comp_choice == 1) or (my_choice == 2 and comp_choice == 2):
        print("Sorry you draw!! Try again.")
    elif (my_choice == 0) and (comp_choice != 1):
        print("You Win")
    elif (comp_choice == 0) and (my_choice != 1):
        print("You lose")
    elif (my_choice == 2) and (comp_choice != 0):
        print("You Win")
    elif (comp_choice == 2) and (my_choice != 0):
        print("You lose")
    elif (my_choice == 1) and (comp_choice != 2):
        print("You Win")
    elif (comp_choice == 1) and (my_choice != 2):
        print("You lose")