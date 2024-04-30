MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

money_given = 0

is_on = True
while is_on:
    available_water = resources['water']
    available_milk = resources['milk']
    available_coffee = resources['coffee']
    cust_request = input("What would you like? (espresso/latte/cappuccino): ")
    if cust_request == 'espresso':
        print(f"The available water is {resources['water']} and coffee is {resources['coffee']} and milk is {resources['milk']}")
        water_value = MENU[cust_request]['ingredients']['water']
        coffee_value = MENU[cust_request]['ingredients']['coffee']
        drink_value = MENU[cust_request]['cost']
        if available_water >= water_value and available_coffee >= coffee_value:
            print(f"Kindly put some money to process your order. {cust_request} costs {drink_value}")
            quarters = int(input("Quarter: "))
            dimes = int(input("Dimes: "))
            nickles = int(input("Nickles: "))
            pennies = int(input("Penies: "))
            money_given = ((0.25*quarters)+(dimes*0.1)+(nickles*0.05)+(pennies*0.01))
            if money_given >= drink_value:
                resources['water'] = available_water - water_value
                resources['coffee'] = available_coffee - coffee_value
                print(f"The remaining water is {resources['water']} and coffee is {resources['coffee']}")
                balance = round((money_given - drink_value),2)
                print(f"Thanks for placing an order with us. You have paid ${money_given} and balance is ${balance}")
            else:
                print(f"Sorry that's not enough money. ${money_given} refunded.")
                money_given = 0
        else:
            print("Sorry, we do not have enough resources to process your order! Kindly check in later.") 

    elif cust_request == 'latte':
        print(f"The available water is {resources['water']} and coffee is {resources['coffee']} and milk is {resources['milk']}")
        water_value = MENU[cust_request]['ingredients']['water']
        milk_value = MENU[cust_request]['ingredients']['milk']
        coffee_value = MENU[cust_request]['ingredients']['coffee']
        total_cost = MENU[cust_request]
        drink_value = MENU[cust_request]['cost']
        if available_water >= water_value and available_coffee >= coffee_value and available_milk >= milk_value:
            print(f"Kindly put some money to process your order. {cust_request} costs {drink_value}")
            quarters = int(input("Quarter: "))
            dimes = int(input("Dimes: "))
            nickles = int(input("Nickles: "))
            pennies = int(input("Penies: "))
            money_given = ((0.25*quarters)+(dimes*0.1)+(nickles*0.05)+(pennies*0.01))
            if money_given >= drink_value:
                resources['water'] = available_water - water_value
                resources['milk'] =available_milk - milk_value
                resources['coffee'] = available_coffee - coffee_value
                print(f"The remaining water is {resources['water']} and coffee is {resources['coffee']} and milk is {resources['milk']}")
                balance = round((money_given - drink_value),2)
                print(f"Thanks for placing an order with us. You have paid ${money_given} and balance is ${balance}")
            else:
                print(f"Sorry that's not enough money. ${money_given} refunded.")
                money_given = 0
        else:
            print("Sorry, we do not have enough resources to process your order! Kindly check in later.")

    elif cust_request == 'cappuccino':
        print(f"The available water is {resources['water']} and coffee is {resources['coffee']} and milk is {resources['milk']}")
        water_value = MENU[cust_request]['ingredients']['water']
        milk_value = MENU[cust_request]['ingredients']['milk']
        coffee_value = MENU[cust_request]['ingredients']['coffee']
        drink_value = MENU[cust_request]['cost']
        if available_water >= water_value and available_coffee >= coffee_value and available_milk >= milk_value:
            print(f"Kindly put some money to process your order. {cust_request} costs {drink_value}")
            quarters = int(input("Quarter: "))
            dimes = int(input("Dimes: "))
            nickles = int(input("Nickles: "))
            pennies = int(input("Penies: "))
            money_given = ((0.25*quarters)+(dimes*0.1)+(nickles*0.05)+(pennies*0.01))
            if money_given >= drink_value:
                resources['water'] = available_water - water_value
                resources['milk'] =available_milk - milk_value
                resources['coffee'] = available_coffee - coffee_value
                print(f"The remaining water is {resources['water']} and coffee is {resources['coffee']} and milk is {resources['milk']}")
                balance = round((money_given - drink_value),2)
                print(f"Thanks for placing an order with us. You have paid ${money_given} and balance is ${balance}")
            else:
                print(f"Sorry that's not enough money. ${money_given} refunded.")
                money_given = 0
        else:
            print("Sorry, we do not have enough resources to process your order! Kindly check in later.")

    elif cust_request == 'report':
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Money: ${money_given}")
    elif cust_request == 'off':
        print("Switching off the Coffee Machine. Goodbye!")
        is_on = False
