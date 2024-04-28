from art import logo
#Adding function
def add(n1,n2):
    return n1+n2

#Subtract function
def subtract(n1,n2):
    return n1-n2

#Multiply function
def multiply(n1,n2):
    return n1*n2

#Division function
def divide(n1,n2):
    return n1/n2

operation = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

def calculator():
    print(logo)
    num1 = float(input("Whats the first number: "))
    #Looping through a list
    for key in operation:
        print(key)

    #Looping through the calculator
    should_continue = True
    while should_continue: 
        operation_num = input("Pick an operation: ")
        num2 = float(input("What's the next number: "))

        calculation_function = operation[operation_num]
        ans = calculation_function(num1,num2)

        print(f'{num1} {operation_num} {num2} = {ans}')

        if input(f"Type 'y' to continue calculating with {ans}, else type 'n' to start a new calculation: ") == 'y':
            num1 = ans
        else:
            print("Goodbye")
            should_continue = False
            #reculsive function
            calculator()

calculator()