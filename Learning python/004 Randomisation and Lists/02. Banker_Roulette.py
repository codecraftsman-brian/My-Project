#Don't change the code below

names_string = input("Give me everybody's names, separated by a comma.\n")
names = names_string.split(',')

#Don't change the code above

#write your code below this line
import random
pay_bill = random.randint(0, len(names)-1)
print(f"{names[pay_bill]} is going to pay the bill for the meal today!")