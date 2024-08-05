# Task 1

# Запрос значення у користувача
number = int(input("Введіть число: "))

# Перевірка, чи є число від’ємним

if number < 0:

    print(f"Введене число: {number}")

else:
    print("Число не є від’ємним")

# Task 2


# Запрос значення у користувача

number = int(input("Введіть ціле число "))

# Перевірка, чи є число менше 20

if number < 20:

    print(f"Число {number} менше 20")

else:
    print(f"Число {number} не менше 20")

# Task 3

# Запрос значення у користувача
number = int(input("Введіть ціле число "))

# Перевірка, чи дорівнює нулю
if number:
    print(f"Число {number} не дорівнює нулю")
else:
    print(f"Число {number} дорівнює нулю")


# Task 4

# Запрос значення у користувача
number = int(input("Введіть ціле число: "))

# Перевірка, чи є число парним чи непарним
result = "Число непарне" if number % 2 else "Число парне"

# Вывод результата
print(result)


# Task 5

# Запит трьох чисел у користувача

number1 = int(input("Введіть перше число: "))
number2 = int(input("Введіть друге число: "))
number3 = int(input("Введіть третє число: "))

max_number = max(number1, number2, number3)

print("Найбільше:", max_number)
