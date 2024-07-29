from collections import defaultdict

def parse_line(line):
    parts = line.strip().split()
    name = ' '.join(parts[1:-2])
    if not parts[-2].endswith("$"):
        raise ValueError(f"Line format is incorrect: {line}")
    amount = float(parts[-2][:-1])
    category = parts[-1]
    return name, amount, category

def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                try:
                    data.append(parse_line(line))
                except ValueError as e:
                    print(f"Error parsing line: {e}")
    return data

def summarize_expenses(data, key):
    totals = defaultdict(float)
    for item in data:
        totals[item[key]] += item[1]  # item[1] is the amount
    return totals

def print_report(title, data):
    print(title)
    for key, value in data.items():
        print(f"{key}: {value:.2f}$")

def person_expenses(data, person):
    total_amount = 0.0
    total_purchases = 0
    for name, amount, _ in data:
        if name == person:
            total_purchases += 1
            total_amount += amount
    return total_purchases, total_amount

# Main program flow
filename = 'hw_10_test.txt'
data = load_data(filename)

print_report("Общая сумма расходов по каждой категории товаров:", summarize_expenses(data, 2))  # 2 is the index for category
print_report("\nСколько денег потратил каждый член семьи:", summarize_expenses(data, 0))  # 0 is the index for
