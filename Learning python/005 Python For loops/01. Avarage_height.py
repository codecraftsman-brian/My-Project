#Don't change the code below

student_height = input("Input a list of surdent heights ").split()
for n in range (0, len(student_height)):
    student_height[n] = int(student_height[n])
print(student_height)

#Don't change the code above

#write your code below this line
total_sum = 0 
sum = 0
for i in student_height:
    sum += i
    total_sum += 1


avarage = int(round((sum / total_sum)))

print(f"The avarage student height is: {avarage}m")
