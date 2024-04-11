#Don't change the code below
print("Welcome to the Love Calculator!")
name1 = input("What is your name? \n")
name2 = input("What is their name? \n")
#Don't change the code above

#Write your code below this line

true_count = 0
love_count = 0

both_names = name1 + name2
both_names = both_names.lower()

t = both_names.count("t")
r = both_names.count("r")
u = both_names.count("u")
e = both_names.count("e")

# true_count = t + r + u + e instead of the if statement

l = both_names.count("l")
o = both_names.count("o")
v = both_names.count("v")
e = both_names.count("e")


if t > 0:
    true_count += t
if r > 0:
    true_count += r
if u > 0:
    true_count += u
if e > 0:
    true_count += e


if l > 0:
    love_count += l
if o > 0:
    love_count += o
if v > 0:
    love_count += v
if e > 0:
    love_count += e


score = str(true_count) + str(love_count)
score = int(score)

if score < 10 or score > 90:
    print(f"Your score is {score}, you go together like coke and mentos.")
elif score > 40  and score < 50:
    print(f"Your score is {score}, you are alright")
else:
    print(f"Your score is {score}")