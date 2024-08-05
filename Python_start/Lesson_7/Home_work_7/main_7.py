# Task_1

def count_words(text):

    words = text.lower().split()
    word_count = {}


    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count


text = input("Enter text: ")
word_count = count_words(text)


print("Word count dictionary:")
for word, count in word_count.items():
    print(f"{word}: {count}")


# Task_2

# Dictionary containing word pairs for translation in both directions
translation_dict = {
    "hello": "привет",
    "world": "мир",
    "cat": "кот",
    "dog": "собака",
    "food": "еда",
    "drink": "напиток",
    "book": "книга",
    "house": "дом",
    "car": "машина",
    "computer": "компьютер",
    "привет": "hello",
    "мир": "world",
    "кот": "cat",
    "собака": "dog",
    "еда": "food",
    "напиток": "drink",
    "книга": "book",
    "дом": "house",
    "машина": "car",
    "компьютер": "computer"
}

# Function to translate a word
def translate_word(word):
    return translation_dict.get(word.lower(), "Translation not found")

# Example usage
while True:
    word = input("Enter a word to translate (or 'exit' to quit): ")
    if word.lower() == 'exit':
        break
    translation = translate_word(word)
    print(f"Translation: {translation}")


# Task_3

contacts = {}

while True:
    action = input("Enter 'add', 'delete', 'get', or 'exit': ").strip().lower()

    if action == 'add':
        name = input("Name: ").strip()
        phone = input("Phone: ").strip()
        contacts[name] = phone
        print(f"Added {name}.")

    elif action == 'delete':
        name = input("Name to delete: ").strip()
        if name in contacts:
            del contacts[name]
            print(f"Deleted {name}.")
        else:
            print("Not found.")

    elif action == 'get':
        name = input("Name to get: ").strip()
        print(f"Phone: {contacts.get(name, 'Not found')}")

    elif action == 'exit':
        break

    else:
        print("Invalid command.")

# Task_4

def convert_currency(amount, from_currency, to_currency, exchange_rates):

    if from_currency == to_currency:
        return amount

    rate = exchange_rates.get((from_currency, to_currency))
    if rate is None:
        raise ValueError(f"Exchange rate for {from_currency}/{to_currency} not found")

    return amount * rate

# Exchange rates
exchange_rates = {
    ("USD", "UAH"): 41.74,
    ("UAH", "USD"): 0.024,
    ("EUR", "USD"): 1.05,
    ("USD", "EUR"): 0.95,
}

# User input
amount = float(input("Enter the amount to convert: "))
from_currency = input("Enter (e.g.): ").upper()
to_currency = input("Enter the currency you are converting to (e.g.): ").upper()

try:
    converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)
    print(f"{amount} {from_currency} is equivalent to {converted_amount:.2f} {to_currency}")
except ValueError as e:
    print(e)