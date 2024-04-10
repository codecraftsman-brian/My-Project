#Don't change the code below

print("welcome to Python Pizza Deliveries!")
size = input("What size pizza do you want? S, M, or L: ")
add_pepperoni = input("Do you want pepperoni? Y or N: ")
extra_cheese = input("Do you want extra cheese? Y or N: ")

#Don't change the code above

#write your code below this line
price = 0

if size == 'S':
    if add_pepperoni == 'Y':
        price += 17
    else:
        price += 15
elif size == 'M':
    if add_pepperoni == 'Y':
        price += 23
    else:
        price += 20
elif size == 'L':
    if add_pepperoni == 'Y':
        price += 28
    else:
        price += 25

if extra_cheese == 'Y':
    price += 1
    print(f"Your final bill is: ${price}.")
else:
    print(f"Your final bill is: ${price}.")