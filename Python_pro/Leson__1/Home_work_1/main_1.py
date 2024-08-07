class Product:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def __str__(self):
        return f"Product(name='{self.name}', price={self.price}, description='{self.description}')"


class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        self.items.append((product, quantity))

    def total_cost(self):
        return sum(product.price * quantity for product, quantity in self.items)

    def __str__(self):
        cart_contents = "\n".join([f"{quantity} x {product}" for product, quantity in self.items])
        return f"Cart:\n{cart_contents}\nTotal cost: {self.total_cost():.2f}"


# Примеры использования:
product1 = Product("Laptop", 1200.99, "A high-performance laptop")
product2 = Product("Smartphone", 699.99, "A latest model smartphone")
product3 = Product("Headphones", 199.99, "Noise-cancelling headphones")

cart = Cart()
cart.add_product(product1, 1)
cart.add_product(product2, 2)
cart.add_product(product3, 3)

print(product1)
print(product2)
print(product3)

print(cart)
