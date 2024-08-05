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

def total_expenses_by_category(filename):
    category_totals = defaultdict(float)
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                try:
                    _, amount, category = parse_line(line)
                    category_totals[category] += amount
                except ValueError as e:
                    print(f"Error parsing line: {e}")
    return category_totals

def total_expenses_by_person(filename):
    person_totals = defaultdict(float)
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                try:
                    name, amount, _ = parse_line(line)
                    person_totals[name] += amount
                except ValueError as e:
                    print(f"Error parsing line: {e}")
    return person_totals

def person_expenses(filename, person):
    total_amount = 0.0
    total_purchases = 0
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                try:
                    name, amount, _ = parse_line(line)
                    if name == person:
                        total_purchases += 1
                        total_amount += amount
                except ValueError as e:
                    print(f"Error parsing line: {e}")
    return total_purchases, total_amount


filename = 'hw_10_test.txt'


category_totals = total_expenses_by_category(filename)
print("Total expenses for each product category:")
for category, total in category_totals.items():
    print(f"{category}: {total:.2f}$")


person_totals = total_expenses_by_person(filename)
print("\nHow much money did each family member spend:")
for person, total in person_totals.items():
    print(f"{person}: {total:.2f}$")


person = input("\nEnter a family member's name to get a detailed report: ").strip()
purchases, total_amount = person_expenses(filename, person)
print(f"\nFamily member {person} made {purchases} purchases totaling {total_amount:.2f}$")
