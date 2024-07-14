def print_sandglass(max_width):
    if max_width % 2 == 0:
        raise ValueError("Maximum width must be an odd number.")

    # Upper half
    for i in range(max_width, 0, -2):
        spaces = (max_width - i) // 2
        stars = i
        print(' ' * spaces + '*' * stars)

    # Lower half
    for i in range(3, max_width + 1, 2):
        spaces = (max_width - i) // 2
        stars = i
        print(' ' * spaces + '*' * stars)


# Read user input and convert to integer
try:
    width = int(input("Enter an odd number for the maximum width of the sandglass: "))
    print_sandglass(width)
except ValueError as e:
    print(e)
