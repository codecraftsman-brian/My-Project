#An increase of alphabets to be able to encrypt the input where shift > 26
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','a', 'b', 'c',
            'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

#TODO-1: Create a function called 'caeser' that takes the 'text' 'shift' and 'direction' as inputs.
def caeser(a, b, c):
    if b == 'encode':        
        encrypt_name = ''
        for i in a:
            position = alphabet.index(i)
            shifted = position + c
            encrypt_name += alphabet[shifted]
        print(f"Here's the encoded result: {encrypt_name}\n")
    elif b == 'decode':
        encrypt_name = ''
        for i in a:
            position = alphabet.index(i)
            shifted = position - c
            encrypt_name += alphabet[shifted]
        print(f"Here's the decoded result: {encrypt_name}\n")

caeser(a=text, b=direction, c=shift)