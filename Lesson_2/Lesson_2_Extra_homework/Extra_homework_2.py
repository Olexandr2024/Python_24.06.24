# Task 1

# Asking the user if they have a driver's license

answer = input("Do you have a driver's license? (yes or no): ")

# Checking the user's answer and printing the appropriate message

if answer.lower() == "yes":
    print("You can drive a car")
elif answer.lower() == "no":
    print("You cannot drive a car")
else:
    print("Please enter 'yes' or 'no'")

# Task 2

# Asking the user for their age

age = int(input("Enter your age: "))

# Checking if the user meets the criteria for getting a driver's license

if age > 18:
    print("You can get a driver's license")
else:
    print("You do not meet the criteria to get a driver's license")

# Task 3

# Asking the user to enter a number
number = int(input("Enter a mumber: "))

# Checking if the number is positive and even

if number > 0 and number % 2 == 0:
    print("The munber is positive and even")
else:
    print("The number does not meet the criteria")

# Task 4

# Asking the user to enter a number
number = int(input("Enter a number: "))

# Checking if the number is divisible by 3 but not by 5
if number % 3 == 0 and number % 5 != 0:
    print("The number is suitable")
else:
    print("The number is not suitable")


