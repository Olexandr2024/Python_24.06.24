# Task 1

# Pre-defined correct password
correct_password = "pas123"

password = input("Enter the password: ")

# Checking if the entered password matches the predefined password

if password == correct_password:
    print("Access granted")
else:
    print("Access denied")


# Task 2

# Asking the user to enter the purchase amount

purchase_amount = float(input("Enter the purchase amount in UAH: "))

# Checking if the purchase amount exceeds 1000 UAH

if purchase_amount > 1000:
    disscount = 0.1 * purchase_amount
    total_amount = purchase_amount - disscount
    print(f"Total amount to pay after 10% discount: {total_amount:.2f} UAH")
else:
    print(f"Total amount to pay: {purchase_amount:.2f} UAH")


# Task 3

# Ask the user to enter the month number
month = int(input("Enter the month number (1-12): "))

# Check the number of days in the month
if month < 1 or month > 12:
    print("Invalid month number. Please enter a number from 1 to 12.")
else:
    # Prompt the user to enter the year
    year = int(input("Enter the year: "))

    # Define the number of days using a dictionary
    days_in_month = {
        1: 31,  # January
        2: 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28,  # February (leap year)
        3: 31,  # March
        4: 30,  # April
        5: 31,  # May
        6: 30,  # June
        7: 31,  # July
        8: 31,  # August
        9: 30,  # September
        10: 31,  # October
        11: 30,  # November
        12: 31  # December
    }

    # Output the number of days in the entered month
    print(f"There are {days_in_month[month]} days in month number {month}.")


# Task 4

# Ask the user to enter the service rating

rating = int(input("Enter the service rating (from 1 to 5): "))

# Determine the corresponding service level message

if rating == 5:
    print("Excellend")
elif rating == 4:
    print("Good")
elif rating == 3:
    print("Satisfactory")
elif rating == 2:
    print("Poor")
elif rating == 1:
    print("Terrible")
else:
    print("Invalid rating entered. Please enter a number from 1 to 5.")


# Task 5

# Ask the user to enter weight (in kilograms) and height (in meters)
weight = float(input("Enter your weight in kilograms: "))
height_str = input("Enter your height in meters (use dot for decimal part): ")

# Replace comma with dot for decimal part (if comma is used)
height_str = height_str.replace(',', '.')

try:
    height = float(height_str)
    # Calculate Body Mass Index (BMI)
    bmi = weight / (height ** 2)

    # Determine the corresponding weight status message based on BMI
    if bmi < 18.5:
        print(f"Your BMI is {bmi:.1f}. You are underweight.")
    elif bmi <= 18.5 and bmi < 25:
        print(f"Your BMI is {bmi:.1f}. You have a normal weight.")
    elif bmi >= 25 and bmi < 30:
        print(f"Your BMI is {bmi:.1f}. You are overweight.")
    else:
        print(f"Your BMI is {bmi:.1f}. You have obesity.")

except ValueError:
    print("Incorrect format for height input. Use dot for decimal part.")

    print(f"Your BMI is {bmi:.1f}. You have obesity.")


