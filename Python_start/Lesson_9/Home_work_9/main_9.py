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
import numpy as np

def find_next_element(seq):
    seq = list(map(int, seq.split(',')))
    diffs = np.diff(seq)
    next_element = seq[-1] + diffs[0] * (diffs[-1] // diffs[0])
    return next_element


sequence = input("Enter a sequence of numbers separated by commas: ")
print(find_next_element(sequence))

# Task_5
def number_to_words(n):
    to_19 = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
    tens = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()

    def get_words(num):
        if num < 20:
            return to_19[num]
        elif num < 100:
            return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + to_19[num % 10])
        else:
            return to_19[num // 100] + ' hundred' + (' ' + get_words(num % 100) if num % 100 else '')

    return get_words(int(n))

def dollars_and_cents_to_words(amount):
    dollars, cents = amount.split(',')
    return f"{number_to_words(dollars)} dollars and {number_to_words(cents)} cents"

# Пример использования
amount = input("Enter the amount in the format dollars,cents (e.g.,): ")
print(dollars_and_cents_to_words(amount))