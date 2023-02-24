def check_number(number: str):
    while True:
        if(number.isdigit()):
            return float(number)

        tmp = number.split('.')
        if (tmp[0].isdigit() and tmp[1].isdigit() and len(tmp) <= 2):
            return float('.'.join(tmp))
        else:
            print("Incorect value")
            number = input()

def function(first_number: float, second_number: float, action: str):
    if action == "add":
        print(f"{first_number} + {second_number} = {first_number + second_number}")
        return False
    elif action == "mul":
        print(f"{first_number} * {second_number} = {first_number * second_number}")
        return False
    elif action == "sub":
        print(f"{first_number} - {second_number} = {first_number - second_number}")
        return False
    elif action == "div":
        if second_number == 0 :
            print("Divide by zero")
            return True
        print(f"{first_number} / {second_number} = {first_number / second_number}")
        return False
    else:
        print("Incorect aciton")
        return True





first_number = check_number(input("Enter the first number \t"))
second_number = check_number(input("Enter the second number \t"))
action  = input("Enter an action \t")

while function(first_number, second_number, action):
    action = input("Try again \t")

print("The end of program")


