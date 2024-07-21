def convert_currency(amount, from_currency, to_currency, exchange_rates):

    if from_currency == to_currency:
        return amount

    rate = exchange_rates.get((from_currency, to_currency))
    if rate is None:
        raise ValueError(f"Exchange rate for {from_currency}/{to_currency} not found")

    return amount * rate

# Exchange rates
exchange_rates = {
    ("USD", "UAH"): 41.74,
    ("UAH", "USD"): 0.024,
    ("EUR", "USD"): 1.05,
    ("USD", "EUR"): 0.95,
}

# User input
amount = float(input("Enter the amount to convert: "))
from_currency = input("Enter (e.g.): ").upper()
to_currency = input("Enter the currency you are converting to (e.g.): ").upper()

try:
    converted_amount = convert_currency(amount, from_currency, to_currency, exchange_rates)
    print(f"{amount} {from_currency} is equivalent to {converted_amount:.2f} {to_currency}")
except ValueError as e:
    print(e)