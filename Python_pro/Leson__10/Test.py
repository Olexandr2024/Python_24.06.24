from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float | int
    category: str


@dataclass
class Clothes:
    name: str
    price: float | int


@dataclass
class Medicine:
    name: str
    price: float | int


class Order:
    def __init__(self):
        self.items = []
        self.quantities = []

    def add_item(self, item, quantity=1):
        self.items.append(item)
        self.quantities.append(quantity)

    def total(self):
        total_price = 0
        total_price_with_tax = 0


        tax_rates = {
            "Product": 0.07,
            "Clothes": 0.15,
            "Medicine": 0.01
        }

        for item, quantity in zip(self.items, self.quantities):
            if isinstance(item, Product):
                category = "Product"
            elif isinstance(item, Clothes):
                category = "Clothes"
            elif isinstance(item, Medicine):
                category = "Medicine"
            else:
                continue

            total_item_price = item.price * quantity
            tax = tax_rates[category]
            total_price += total_item_price
            total_price_with_tax += total_item_price * (1 + tax)

        return total_price, total_price_with_tax



order = Order()
order.add_item(Product("Apple", 10, "Product"), 3)
order.add_item(Clothes("T-Shirt", 20), 2)
order.add_item(Medicine("Aspirin", 5), 5)

total, total_with_tax = order.total()
print(f"Total without tax: {total}")
print(f"Total with tax: {total_with_tax}")

