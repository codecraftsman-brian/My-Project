#Don't change the code below
row1 = ['✨','✅','❤️']
row2 = ['✨','✅','❤️']
row3 = ['✨','✅','❤️']
map = [row1, row2, row3]
print(f"{row1}\n {row2} \n {row3}")
position = input("Where do you want to put the treasure\n")
#Don't change the code above2

#write your code below this line
vertical = int(position[0])
horizontal = int(position[1])

map[horizontal-1][vertical-1] = 'X'

print(f"{row1}\n {row2} \n {row3}")

