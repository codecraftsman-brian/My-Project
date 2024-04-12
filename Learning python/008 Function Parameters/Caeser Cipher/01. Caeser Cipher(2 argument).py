alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

#TODO-1: Create a function called 'encrypt' that takes the 'text' and 'shift' as inputs.

#The function that encrypt the passed input
def encrypt(a,b):
    encrypt_name = []
    for i in a:
        position = alphabet.index(i)
        shifted = position + b
        encrypted = alphabet[shifted]
        encrypt_name.append(encrypted)
        word = ''.join(encrypt_name)
    print(f"Here's the encoded result: {word}\n")

#The function that decrypt the passed input
def decrypt(a,b):
    decrypt_name = []
    for i in a:
        position = alphabet.index(i)
        shifted = position - b
        encrypted = alphabet[shifted]
        decrypt_name.append(encrypted)
        word = ''.join(decrypt_name)
    print(f"Here's the decoded result: {word}\n")

#Logic to determine if to encode or decode the passed input
if direction == 'encode':        
    encrypt(a=text,b=shift)
elif direction == 'decode':
    decrypt(a=text,b=shift)
else:
    print('Invalid!!')

