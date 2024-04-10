#Input the year you want to check
year = int(input("Which year do you want to check? "))

#Logic to check if the year is a leap year
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print("Leap year.")
else:
    print("Not leap year.")