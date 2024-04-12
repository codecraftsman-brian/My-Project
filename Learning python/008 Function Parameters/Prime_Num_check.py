#input the no. you want to check if it's a prime no.
n = int(input("Check this number: "))

#The function to checking if the passed no. is a prime no.
def prime_checker(number=n):
    prime_num = []
    for i in range(2,number+1):
        if i == 5 or i / 1 == i and  i % 5 != 0 and  i % 7 != 0 and i/i == 1 and i%2 == 1  and i%3 != 0 or i<=3 :
            prime_num.append(i)
    if n in prime_num:
        print("It's a prime number.")
    else:
        print("It's not a prime number.")

#Calling the function
prime_checker(n)