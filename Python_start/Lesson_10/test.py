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
