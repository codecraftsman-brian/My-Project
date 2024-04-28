alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#TODO-1: Create a function called 'encrypt' that takes the 'text' and 'shift' as inputs.

#The function that encrypt the passed input
def encrypt(a,b):
    encrypt_name = []
    for i in a:
        position = alphabet.index(i)
        shift_key = position + b
        encrypted = alphabet[shift_key]
        encrypt_name.append(encrypted)
        word = ''.join(encrypt_name)
    print(f"Here's the encoded result: {word}\n")

#The function that decrypt the passed input
def decrypt(a,b):
    decrypt_name = ""
    for i in a:
        position = alphabet.index(i)
        shift_key = position - b
        encrypted = alphabet[shift_key]
        decrypt_name += encrypted
    print(f"Here's the decoded result: {decrypt_name}\n")

#Logic to determine if to encode or decode the passed input
direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
if direction == 'encode': 
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))       
    encrypt(a=text,b=shift)
elif direction == 'decode':
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    decrypt(a=text,b=shift)
else:
    print('Invalid!!')

