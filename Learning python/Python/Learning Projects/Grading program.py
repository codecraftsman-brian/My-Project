student_scores = {
  "Harry": 81,
  "Ron": 78,
  "Hermione": 99, 
  "Draco": 74,
  "Neville": 62,
}
#Create an empty dictionary called student_grades.
student_grades = {}

#code below to add the grades to student_grades.👇
for key, value in student_scores.items():
    if value > 90:
        student_grades[key] = "Outstanding"
    elif value > 80 and value <= 90:
        student_grades[key] = "Exceeds Expectations"
    elif value > 70 and value <= 80:
        student_grades[key] = "Acceptable"
    else:
        student_grades[key] = "Fail"

#Prints out the new dict with the changed values.
print(student_grades)