import re
from collections import defaultdict

def parse_line(line):
    match = re.match(r'(\d+)\s+([A-Za-z ]+)\s+(\d+\.\d+)\$\s+(\w+)', line.strip())
    if match:
        number = match.group(1)
        name = match.group(2).strip()
        amount = float(match.group(3))
        category = match.group(4).strip()
        return name, amount, category
    else:
        raise ValueError(f"Line format is incorrect: {line}")

def load_data(filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                yield parse_line(line)

def total_expenses_by_category(data):
    category_totals = defaultdict(float)
    for _, amount, category in data:
        category_totals[category] += amount
    return category_totals

def total_expenses_by_person(data):
    person_totals = defaultdict(float)
    for name, amount, _ in data:
        person_totals[name] += amount
    return person_totals

def person_expenses(filename, person):
    total_amount = 0.0
    total_purchases = 0
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                name, amount, _ = parse_line(line)
                if name == person:
                    total_purchases += 1
                    total_amount += amount
    return total_purchases, total_amount

# File name
filename = 'hw_10_test.txt'

# Calculating total expenses by category and by person
data = load_data(filename)

category_totals = total_expenses_by_category(load_data(filename))
print("Total expenses for each product category:")
for category, total in category_totals.items():
    print(f"{category}: {total:.2f}$")

person_totals = total_expenses_by_person(load_data(filename))
print("\nHow much money did each family member spend:")
for person, total in person_totals.items():
    print(f"{person}: {total:.2f}$")

# Getting detailed report for a specific family member
person = input("\nEnter a family member's name to get a detailed report: ").strip()
purchases, total_amount = person_expenses(filename, person)
print(f"\nFamily member {person} did {purchases} total purchases for {total_amount:.2f}$")
