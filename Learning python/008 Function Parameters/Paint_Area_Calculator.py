#write your code below this line
import math
def paint_calc(height,width,cover):
    area = height * width

    total_cans = math.ceil(area / cover)

    print(f"You'll need {total_cans} cans of paint")

#write your code above this line

#Don't change the code below
test_h = int(input("Hieght of wall: "))
test_w = int(input("Width of wall: "))

coverage = 5

paint_calc(height=test_h, width=test_w, cover=coverage)