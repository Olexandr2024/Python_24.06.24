# Task 1
# Запитуємо ім'я користувача
name = input("Введите ваше имя: ")

# Виводимо вітання
print(f'Привіт, {name}!')


# Task 2

# Запитуємо п'ять цілих значень від користувача та зберігаємо їх у списку
numbers = [int(input(f"Введите число {i+1}: ")) for i in range(5)]

# Знаходимо мінімальне значення, максимальне значення та середнє значення
min_value = min(numbers)
max_value = max(numbers)
average_value = sum(numbers) / len(numbers)

# Виводимо результати
print(f"Мінімальне значення: {min_value}")
print(f"Максимальне значення: {max_value}")
print(f"Середнє значення: {average_value}")

# Task 3

# Запит введення чисел від користувача
x = float(input("Введите первое число: "))
y = float(input("Введите второе число: "))

# Виведення результатів арифметичних операцій
print(f"{x} + {y} = {x + y}")
print(f"{x} - {y} = {x - y}")
print(f"{x} * {y} = {x * y}")
print(f"{x} / {y} = {x / y}")
print(f"{x} // {y} = {x // y}")
print(f"{x} % {y} = {x % y}")


# Task 4

import math

radius = float(input("Введите радиус окружности: "))

diameter = 2 * radius
circumference = 2 * math.pi * radius
area = math.pi * radius ** 2

print(f"Диаметр: {diameter}")
print(f"Длина окружности: {circumference}")
print(f"Площадь окружности: {area}")

# Task 5

# Початкова інвестована сума
p = 1000

# Річна норма прибутку (10%)
r = 0.10

# Кількість років
years = [10, 20, 30]

# Розрахунок суми на депозиті для кожного зазначеного року
for n in years:
    a = p * (1 + r) ** n
    print(f"Через {n} років ви матимете: ${a:.2f}")


# Task 6

# Запит обмінного курсу від користувача
exchange_rate = float(input("Введіть поточний обмінний курс долара до гривні: "))

# Запит суми в доларах від користувача
amount_usd = float(input("Введіть суму в доларах для конвертації: "))

# Конвертація в гривні
amount_uah = amount_usd * exchange_rate

# Виведення результату
print(f"{amount_usd} доларів = {amount_uah:.2f} гривень за обмінним курсом {exchange_rate}")

# Task 7

# Запит від користувача для введення тризначного числа
number = int(input("Введіть тризначне ціле число: "))

# Отримання окремих цифр
digit1 = number // 100    # перша цифра числа
digit2 = (number // 10) % 10  # друга цифра числа
digit3 = number % 10      # третя цифра числа

# Виведення кожної цифри в окремому рядку
print(digit1)
print(digit2)
print(digit3)
