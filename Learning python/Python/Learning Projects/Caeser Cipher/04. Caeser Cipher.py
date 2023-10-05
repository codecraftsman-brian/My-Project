#Importing a art file to our working space
import art

#Import and print the logo from art.py when the program starts.
my_logo = art.logo
print(my_logo)
#An increase of alphabets to be able to encrypt the input where shift > 26
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#Create a function called 'caeser' that takes the 'text' 'shift' and 'direction' as inputs.
def caeser(a, b, c):
    if b == 'encode':        
        encrypt_name = ''
        for i in a:
            #Logic checking if the input contains a non-alphabetic.
            if i in alphabet:
                position = alphabet.index(i)
                shifted = position + c
                encrypt_name += alphabet[shifted]
            else:
                encrypt_name += i
        print(f"Here's the encoded result: {encrypt_name}\n")
    elif b == 'decode':
        encrypt_name = ''
        for i in a:
            #Logic checking if the input contains a non-alphabetic.
            if i in alphabet:            
                position = alphabet.index(i)
                shifted = position - c
                encrypt_name += alphabet[shifted]
            else:
                encrypt_name += i
        print(f"Here's the decoded result: {encrypt_name}\n")
    else:
        print('Invalid')

#TODO-4: Can you figure out a way to ask the user if they want to restart the cipher program?
#e.g. Type 'yes' if you want to go again. Otherwise type 'no'.
#If they type 'yes' then ask them for the direction/text/shift again and call the caesar() function again?
#Hint: Try creating a while loop that continues to execute the program if the user types 'yes'. 

#TODO-2: What if the user enters a shift that is greater than the number of letters in the alphabet?
#Try running the program and entering a shift number of 45.
#Add some code so that the program continues to work even if the user enters a shift number greater than 26. 
#Hint: Think about how you can use the modulus (%).
while true:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    #Handles shift greater than than the length of the list 
    shift = shift % 25

    caeser(a=text, c=shift, b=direction)

    result = input("Type 'Yes' if you want to go again. Otherwise type 'No':\n")

    if result == 'No':
            print('Goodbye')
            break
