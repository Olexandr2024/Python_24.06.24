class Product:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def __str__(self):
        """
        Returns a string representation of the product.

        Returns:
            A string that describes the product with its name, price, and description.
        """
        return f"{self.name} - ${self.price:.2f}: {self.description}"


class Discount:
    def apply(self, price):
        """
        Applies the discount to the given price.

        Args:
            price: The original price before the discount.

        Returns:
            The price after the discount is applied.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class PercentageDiscount(Discount):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply(self, price):
        """
        Applies a percentage discount to the given price.

        Args:
            price: The original price before the discount.

        Returns:
            The price after the percentage discount is applied.
        """
        return price - (price * (self.percentage / 100))


class FixedAmountDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, price):
        """
        Applies a fixed amount discount to the given price.

        Args:
            price: The original price before the discount.

        Returns:
            The price after the fixed amount discount is applied.
        """
        return max(0, price - self.amount)


class DiscountMixin:
    def apply_discount(self, discount: Discount):
        """
        Applies the given discount to each product in the cart.

        Args:
            discount: An instance of Discount to be applied to each product.
        """
        for i, (product, quantity) in enumerate(self.items):
            discounted_price = discount.apply(product.price)
            self.items[i] = (Product(product.name, discounted_price, product.description), quantity)


class PaymentProcessor:
    def pay(self, amount):
        """
        Processes a payment of the given amount.

        Args:
            amount: The total amount to be paid.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number, card_holder, cvv, expiry_date):
        self.card_number = card_number
        self.card_holder = card_holder
        self.cvv = cvv
        self.expiry_date = expiry_date

    def pay(self, amount):
        """
        Processes the payment using the credit card.

        Args:
            amount: The total amount to be paid.
        """
        print(f"Processing credit card payment of ${amount:.2f}")
        print(f"Card Number: {self.card_number}")
        print(f"Card Holder: {self.card_holder}")
        print(f"Expiry Date: {self.expiry_date}")
        print("Payment successful!\n")


class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        """
        Processes the payment using PayPal.

        Args:
            amount: The total amount to be paid.
        """
        print(f"Processing PayPal payment of ${amount:.2f}")
        print(f"PayPal Account: {self.email}")
        print("Payment successful!\n")


class BankTransferProcessor(PaymentProcessor):
    def __init__(self, account_number, account_holder):
        self.account_number = account_number
        self.account_holder = account_holder

    def pay(self, amount):
        """
        Processes the payment using a bank transfer.

        Args:
            amount: The total amount to be paid.
        """
        print(f"Processing bank transfer of ${amount:.2f}")
        print(f"Bank Account: {self.account_number}")
        print(f"Account Holder: {self.account_holder}")
        print("Payment successful!\n")


class Cart(DiscountMixin):
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        """
        Adds a product and its quantity to the cart.

        Args:
            product: An instance of Product to add to the cart.
            quantity: The quantity of the product to add.
        """
        self.items.append((product, quantity))

    def total_cost(self):
        """
        Calculates the total cost of all products in the cart.

        Returns:
            The total cost as a float.
        """
        return sum(product.price * quantity for product, quantity in self.items)

    def pay(self, payment_processor: PaymentProcessor):
        """
        Processes payment for the total cost of the cart.

        Args:
            payment_processor: An instance of a PaymentProcessor to handle the payment.
        """
        total = self.total_cost()
        payment_processor.pay(total)

    def __str__(self):
        """
        Returns a string representation of the cart contents and total cost.

        Returns:
            A string that lists all items in the cart and their total cost.
        """
        cart_contents = "\n".join([f"{quantity} x {product}" for product, quantity in self.items])
        return f"Cart:\n{cart_contents}\nTotal cost: ${self.total_cost():.2f}"


def main():
    """
    The main function that demonstrates creating products, adding them to a cart, applying discounts,
    and processing payments using different payment processors.

    Args:
        None

    Returns:
        None
    """
    # Creating instances of the Product class
    product1 = Product("Laptop", 1500.00, "A high-end gaming laptop")
    product2 = Product("Mouse", 50.00, "A wireless mouse")
    product3 = Product("Keyboard", 100.00, "A mechanical keyboard")

    # Creating an instance of the Cart class and adding products
    cart = Cart()
    cart.add_product(product1, 1)
    cart.add_product(product2, 2)
    cart.add_product(product3, 1)

    print(cart)
    print("Total cost:", cart.total_cost())

    # Applying different types of discounts
    percentage_discount = PercentageDiscount(10)
    fixed_amount_discount = FixedAmountDiscount(100)

    cart.apply_discount(percentage_discount)
    print(cart)
    print("Total cost after percentage discount:", cart.total_cost())

    cart.apply_discount(fixed_amount_discount)
    print(cart)
    print("Total cost after fixed amount discount:", cart.total_cost())

    # Using different payment systems
    credit_card_processor = CreditCardProcessor("1234-5678-9876-5432", "John Doe", "123", "12/25")
    paypal_processor = PayPalProcessor("john.doe@example.com")
    bank_transfer_processor = BankTransferProcessor("987654321", "John Doe")

    cart.pay(credit_card_processor)
    cart.pay(paypal_processor)
    cart.pay(bank_transfer_processor)


if __name__ == "__main__":
    main()
