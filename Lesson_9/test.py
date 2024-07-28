from collections import defaultdict
expenses = [
    '1 Bob Simson 19.58$ decorations',
    '2 Mary 66.7$ food',
    '3 Mary 98.91$ toys',
    '4 Aleksa 72.29$ drinks',
    '5 Maria Simson 84.48$ food',
    '6 Aleksa 100.41$ accessories',
    '7 Mary 19.9$ accessories',
    '8 Bob Simson 83.88$ drinks',
    '9 Bob Simson 58.21$ instruments',
    '10 Maria Simson 20.61$ accessories'
]

def expenses_by_categories(expenses):
    category_totals = defaultdict(float)
    for entry in expenses:
        parts = entry.split()
        category_totals[parts[-1]] += float(parts[-2].replace('$', ''))
    return {category: round(total, 2) for category, total in category_totals.items()}

def expenses_by_users(expenses):
    user_totals = defaultdict(float)
    for entry in expenses:
        parts = entry.split()
        user_totals[' '.join(parts[1:-2])] += float(parts[-2].replace('$', ''))
    return {user: round(total, 2) for user, total in user_totals.items()}


categories_totals = expenses_by_categories(expenses)
users_totals = expenses_by_users(expenses)

print("Expenses by category:", categories_totals)
print("Costs by user:", users_totals)
