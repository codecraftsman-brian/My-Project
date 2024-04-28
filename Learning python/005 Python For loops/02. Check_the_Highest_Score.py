#Don't change the code below

student_score = input("Input a list of student score ").split()
for n in range (0, len(student_score)):
    student_score[n] = int(student_score[n])
print(student_score)

#Don't change the code above

#write your code below this line
total_len = 1
x = 0
max_num = 0
for i in student_score:
    if student_score[x] > student_score[total_len]:
        del student_score[total_len]
        print(student_score)
        max_num = student_score[x]
    else:
        print(student_score[x])
        
    total_len += 1
    x += 1

print(f"The highest score in the class is: {max_num}")