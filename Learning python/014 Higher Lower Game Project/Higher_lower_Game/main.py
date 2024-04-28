import art as art
from game_data import data
import os 

#Kicks of the while loop
count = 0
list_length = len(data)

#Picks a set from a dictionary
compare_A = 0
compare_B = 1

score = 0

#will continue looping until the dataset id over
while count < list_length:
    print(art.logo)
    if score != 0:
        print(f"Congratulations! You win. Your score is, {score}.")
    print(f"Compare A: {data[compare_A]['name']}, a {data[compare_A]['description']} from {data[compare_A]['country']}.")
    print(art.vs)
    print(f"Aginist B: {data[compare_B]['name']}, a {data[compare_B]['description']} from {data[compare_B]['country']}.")
    
    compare = input("Who has more followers? Type 'A' or 'B': ")

    follower_A = data[compare_A]['follower_count']
    follower_B = data[compare_B]['follower_count']

    if compare == 'A' and follower_A > follower_B:
        score += 1
    elif compare == 'A' and follower_A < follower_B:
        os.system('cls')
        print(art.logo)
        print (f"Sorry you lose! Your final score is, {score}.")
        break
    elif compare == 'B' and follower_A < follower_B:
        score += 1
    elif compare == 'B' and follower_A > follower_B:
        os.system('cls')
        print(art.logo)
        print (f"Sorry you lose! Your final score is, {score}.")
        break

    count += 1
    compare_A += 1
    compare_B += 1

# Enhance the code so that the user can restart the program
# Do you want to restart the game?


