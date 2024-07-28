def calculate_tax(income, tax_rate):

    tax_amount = income * (tax_rate / 100)
    return tax_amount


income = 50000  # Example income
tax_rate = 20   # Example tax rate
tax = calculate_tax(income, tax_rate)
print(f"The calculated tax amount is: {tax}")

# Task_2
import random
import string


def generate_password(length, include_special_chars):

    characters = string.ascii_letters + string.digits + string.punctuation * include_special_chars


    password = ''.join(random.choice(characters) for _ in range(length))
    return password

length = 12  # Example password length
include_special_chars = True  # Include special characters
password = generate_password(length, include_special_chars)
print(f"Generated password: {password}")

# Task_3
def is_palindrome(num):
    return str(num) == str(num)[::-1]

def largest_palindrome_product():

    products = ((i, j, i * j) for i in range(100, 1000) for j in range(i, 1000))
    palindromes = filter(lambda x: is_palindrome(x[2]), products)
    largest_palindrome = max(palindromes, key=lambda x: x[2])

    return largest_palindrome[2], (largest_palindrome[0], largest_palindrome[1])


largest_palindrome, (factor1, factor2) = largest_palindrome_product()
print(f"The largest palindrome is: {largest_palindrome}")
print(f"It is the product of: {factor1} and {factor2}")

# Task_4

