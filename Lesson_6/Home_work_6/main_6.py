# Task_1
input_string = input(("Enter a string: "))

count_b = input_string.lower().count('b')

print(f"The number of 'b' in the string is: {count_b}")

# Task_2

name = input('Enter a name: ')

words = name.split()

if all(word.istitle() and word.isalpha() for word in words):
    print(f"The name '{name}' is valid")
else:
    print(f"The name '{name}' is not valid")

# Task_3

input_string = input('Enter a string: ')

total_sum = sum(ord(char) for char in input_string)

print(f"The sum of all character codes in the string is: {total_sum}")

# Task_4

import math

for i in range(2, 12):
    print(f"{math.pi:.{i}f}")


# Task_5

text = input("Enter text: ")

words = text.split()

longest_word = max(words, key=len)

print(f"Lost word: {longest_word}")

# Task_6

text = input("Enter a row: ")

shortest_word = text

for word_length in range(1, len(text) // 2 + 1):
    word = text[:word_length]
    if text == word * (len(text) // word_length):
        shortest_word = word
        break
print(f"Vovochka writing the word - '{shortest_word}'")

# Task_7
def clean_html_tags(text):
    in_tag = 0
    result = ''
    i = 0

    while i < len(text):
        if text[i] == '<':
            in_tag += 1
        elif text[i] == '>':
            in_tag -= 1
        elif in_tag == 0:
            result += text[i]
        i += 1

    while '<' in result:
        start = result.find('<')
        end = result.find('>')
        if start != -1 and end != -1:
            result = result[:start] + result[end + 1:]

    return result


# Example usage
html_text = '''
<div id="rcnt" style="clear:both;position:relative;zoom:1">
'''

cleaned_text = clean_html_tags(html_text)
print("Cleared text:")
print(cleaned_text)