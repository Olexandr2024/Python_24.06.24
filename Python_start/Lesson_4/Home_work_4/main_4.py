# Task 1
def is_lucky_ticket(number):
    # Convert to string and check sums
    number_str = str(number)
    return len(number_str) == 4 and sum(map(int, number_str[:2])) == sum(map(int, number_str[2:]))

# Input list of numbers
numbers = map(int, input("Enter four-digit numbers separated by spaces: ").split())

# Check and print result for each number
for number in numbers:
    result = "is" if is_lucky_ticket(number) else "is not"
    print(f"{number} {result} a lucky ticket.")

# Task 2
def is_palindrome(number):
    # Convert the number to a string

    number_str = str(number)

    # Check if the string is the same forwards and backwards
    return number_str == number_str[::-1]

# Ask the user to enter a six-digit number
number = input("Enter a number: ")

# Check if the number is a six-digit number and if it is a palindrome

if number.isdigit():
    if is_palindrome(number):
        print(f"{number} is a palindrome.")
    else:
        print(f"{number} is not a palindrome.")
else:
    print("Please enter a valid number.")

# Task 3

def is_pount_in_circle(x, y, radius):
    # Calculate the square of the distance from the origin to the point (x, y)
    distance_squared = x ** 2 + y ** 2
    # Check if the squared distance is less than or equal to the squared radius
    return distance_squared <= radius**2

# Radius of the circle
radius = 4

# Input coordinates of the point from the user

x = float(input("Enter the x-coordinate of the point: "))
y = float(input("Enter the y-coordinate of the point: "))

# Check if the point is inside the circle and print the result

if is_pount_in_circle(x, y, radius):
    print(f"The point ({x}, {y}) is inside the circle with radius {radius}.")
else:
    print(f"The point ({x}, {y}) is outside the circle with radius {radius}.")
