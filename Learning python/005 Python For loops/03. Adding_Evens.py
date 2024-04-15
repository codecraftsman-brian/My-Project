#write your code below this line
my_number = 0
total = 0 

#route 1 
for i in range(1,101):# range(2,101, 2) is recommended
    if i % 2 == 0:
        my_number += i

#or route 2
for i in range(2,101, 2):
    total += i

print(f"Your even total number is: {my_number}")
print(f"Your even total number is: {total}")