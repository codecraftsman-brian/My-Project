#Don't change the code below

row1 = ['✨','✅','❤️']
row2 = ['✨','✅','❤️']
row3 = ['✨','✅','❤️']
map = [row1, row2, row3]
#print(f"{row1}\n {row2} \n {row3}")
position = input("Where do you want to put the treasure?")

#Don't change the code above

#write your code below this line
row1.pop(position[0])
row1.insert(position[0],'X')
print(row1)

