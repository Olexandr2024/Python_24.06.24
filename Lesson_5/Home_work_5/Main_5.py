# Task_1
def main():
    for number in range(1, 101):
        if number % 7 == 0:
            print(number)

if __name__ == "__main__":
    main()

# Task_2
def main():
    summa = 0
    count = 0

    for number in range(1, 100):
        if number % 2 != 0:  # Check if the number is odd
            summa += number
            count += 1

    print(f"Sum of odd numbers from 1 to 99: {summa}")
    print(f"Count of odd numbers from 1 to 99: {count}")


if __name__ == "__main__":
    main()


# Task_3

def main():
    num = 1
    count = 0

    while num <= 200:
        print(num, end='')
        num += 1
        count += 1

        if count == 5:
            print()
            count = 0

if __name__ == "__main__":
    main()

# Task_4

def main():
    n = int(input("Enter a number to calculate its factorial: "))

    factorial = 1

    for i in range(1, n + 1):
        factorial *= i

    print(f"The factorial of {n} is {factorial}")

if __name__ == "__main__":
        main()


# Task_5

def multiplication_table_5():
    for i in range(1, 11):
        print(f"{i} x 5 = {i * 5}")

if __name__ == "__main__":
    multiplication_table_5()


# Task_6

def draw_rectangle(width, height):
    for i in range(height):
        if i == 0 or i == height - 1:
            print('*' * width)
        else:
            print('*' + ' ' * (width - 2) + '*')

def main():
    width = int(input("Enter the width of the rectangle: "))
    height = int(input("Enter the height of the rectangle: "))
    draw_rectangle(width, height)


if __name__ == "__main__":
    main()


# Task_7

numbers = [0, 5, 2, 4, 7, 1, 3, 19]

odd_count = sum(1 for num in numbers if num % 2 !=0)

print(f"Number of unpaired numbers in the list: {odd_count}")

# Task_8
import random

first_list = [random.randint(1, 10) for _ in range(4)]

second_list = first_list + [x * 2 for x in first_list]

print("First list:", first_list)
print("Other list:", second_list)

# Task_9
salaries = [3000, 3200, 3500, 3800, 4000, 4200, 3800, 3900, 4100, 4300, 4000, 4200]

print("List of salaries for the month:", salaries)

average_salary = sum(salaries) / len(salaries)

print(f"Average monthly salary: {average_salary:.2f}")

# Task_10

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]


print("Matrix:")
for row in matrix:
    print(row)


total_sum = 0
for row in matrix:
    total_sum += sum(row)


print(f"Sum of matrix elements: {total_sum}")

# Task_11

original_list = [7, 2, 9, 4]

reversed_list = original_list[::-1]

print(f"Reversed list: {reversed_list}")

# Task_12


for num in range(2, 101):



    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break


    if is_prime:
        print(num)


# Task_13

def print_sandglass(max_width):
    if max_width % 2 == 0:
        raise ValueError("Maximum width must be an odd number.")


    for i in range(max_width, 0, -2):
        spaces = (max_width - i) // 2
        stars = i
        print(' ' * spaces + '*' * stars)


    for i in range(3, max_width + 1, 2):
        spaces = (max_width - i) // 2
        stars = i
        print(' ' * spaces + '*' * stars)



try:
    width = int(input("Enter an odd number for the maximum width of the sandglass: "))
    print_sandglass(width)
except ValueError as e:
    print(e)





