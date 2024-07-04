# Task 1

# Receiving the apartment number from the user
apartment_number = int(input('Enter apartment number:'))

# Defining the parameters of the house

floors = 9
entrances = 4
apartment_per_floor = 4

# Check if the apartment number corresponds to the range of apartments in the building

if 1 <= apartment_number <= (floors * entrances * apartment_per_floor):
    entrances_number = (apartment_number - 1) // (floors * apartment_per_floor) +1
    floors_number = ((apartment_number - 1) % (floors * apartment_per_floor)) // apartment_per_floor + 1
    apartment_per_floor = (apartment_number - 1) % apartment_per_floor + 1

    print(f'Entrance: {entrances_number}, Floor: {floors_number}, Floor number: {apartment_per_floor}')
else:
    print('There is no such apartment in this building.')

# Task 2

# Getting the year number from the user

year = int(input('Enter year: '))

# Determination of leap year

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f'{year} h is leapfrog.')
else:
    print(f'{year} h is not a leap year.')

# Task 3

# Getting the lengths of the sides of the triangle from the user

A = float(input('Enter the length of side A: '))
B = float(input('Enter the length of side A: '))
C = float(input('Enter the length of side A: '))

# Checking the conditions for the existence of a triangle

if A + B > C and A + C > B and B + C > A:
    print("Such a triangle exists.")
else:
    print("Such a triangle does not exist.")
