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
    data = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                data.append(parse_line(line))
    return data

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

def person_expenses(data, person):
    total_amount = 0.0
    total_purchases = 0
    for name, amount, _ in data:
        if name == person:
            total_purchases += 1
            total_amount += amount
    return total_purchases, total_amount

# Loading data from a file
filename = 'hw_10_test.txt'
data = load_data(filename)


category_totals = total_expenses_by_category(data)
print("Total expenses for each product category:")
for category, total in category_totals.items():
    print(f"{category}: {total:.2f}$")


person_totals = total_expenses_by_person(data)
print("\nHow much money did each family member spend")
for person, total in person_totals.items():
    print(f"{person}: {total:.2f}$")


person = input("\nEnter a family member's name to get a detailed report: ").strip()
purchases, total_amount = person_expenses(data, person)
print(f"\nFamily member {person} did {purchases} total purchases {total_amount:.2f}$")
