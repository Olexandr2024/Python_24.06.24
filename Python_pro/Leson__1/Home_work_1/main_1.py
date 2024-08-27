import re
from datetime import datetime

class LoggingMixin:
    """Mixin class to provide logging functionality for actions in Product and Cart classes."""
    def log(self, message):
        """Logs a message to the console or a file."""
        print(f"LOG: {message}")

class InvalidPriceError(Exception):
    """Custom exception raised when an invalid price (negative or zero) is set for a product."""
    def __init__(self, price):
        super().__init__(f"Invalid price: {price}. Price must be greater than 0.")

class InvalidQuantityError(Exception):
    """Custom exception raised when an invalid quantity (negative or zero) is added to the cart."""
    def __init__(self, quantity):
        super().__init__(f"Invalid quantity: {quantity}. Quantity must be greater than 0.")

class InvalidCardDetailsError(Exception):
    """Custom exception for invalid card details."""
    def __init__(self, message):
        super().__init__(f"Invalid card details: {message}")

class Product(LoggingMixin):
    """Represents a product in the store."""
    def __init__(self, name, price, description):
        if price <= 0:
            raise InvalidPriceError(price)
        self.name = name
        self.price = price
        self.description = description
        self.log(f"Created product: {self.name}, Price: {self.price:.2f}")

    def __str__(self):
        return f"Product(name='{self.name}', price={self.price:.2f}, description='{self.description}')"

    def update_price(self, new_price):
        """Updates the price of the product."""
        if new_price <= 0:
            raise InvalidPriceError(new_price)
        self.log(f"Price for {self.name} updated from {self.price:.2f} to {new_price:.2f}")
        self.price = new_price

class Discount:
    """Base class for discounts."""
    def apply(self, price):
        """Applies the discount to the given price."""
        raise NotImplementedError("This method should be overridden by subclasses")

class PercentageDiscount(Discount, LoggingMixin):
    """Applies a percentage discount to a price."""
    def __init__(self, percentage):
        self.percentage = percentage

    def apply(self, price):
        """Calculates the discounted price based on a percentage discount."""
        discount_amount = price * (self.percentage / 100)
        new_price = price - discount_amount
        self.log(f"Applied {self.percentage}% discount: Old Price: {price:.2f}, New Price: {new_price:.2f}")
        return new_price

class FixedAmountDiscount(Discount, LoggingMixin):
    """Applies a fixed amount discount to a price."""
    def __init__(self, amount):
        self.amount = amount

    def apply(self, price):
        """Calculates the discounted price by subtracting a fixed amount."""
        new_price = max(0, price - self.amount)
        self.log(f"Applied fixed discount: {self.amount:.2f}, Old Price: {price:.2f}, New Price: {new_price:.2f}")
        return new_price

class DiscountMixin:
    """Mixin class to apply discounts to all products in the cart."""
    def apply_discount(self, discount: Discount):
        """Applies the given discount to each product in the cart."""
        for i, (product, quantity) in enumerate(self.items):
            discounted_price = discount.apply(product.price)
            self.items[i] = (Product(product.name, discounted_price, product.description), quantity)
        self.log(f"Discount applied to all products in the cart using {discount.__class__.__name__}.")

class CartIterator:
    """Iterator class for Cart items."""
    def __init__(self, cart):
        self._cart = cart
        self._index = 0

    def __iter__(self):
        """Returns the iterator object itself."""
        return self

    def __next__(self):
        """Returns the next item in the cart or raises StopIteration."""
        if self._index < len(self._cart.items):
            result = self._cart.items[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

class Cart(DiscountMixin, LoggingMixin):
    """Represents a shopping cart that holds products and handles payments."""
    def __init__(self):
        self.items = []
        self.log("Initialized an empty shopping cart.")

    def add_product(self, product, quantity):
        """Adds a product and its quantity to the cart."""
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        self.items.append((product, quantity))
        self.log(f"Added product: {product.name}, Quantity: {quantity} to the cart.")

    def total_cost(self):
        """Calculates the total cost of the items in the cart."""
        total = sum(product.price * quantity for product, quantity in self.items)
        self.log(f"Total cost calculated: {total:.2f}")
        return total

    def pay(self, payment_processor):
        """Processes the payment for the total cost of the cart using the specified payment processor."""
        total = self.total_cost()
        payment_processor.pay(total)
        self.log(f"Payment of ${total:.2f} processed using {payment_processor.__class__.__name__}.")

    def __str__(self):
        """Returns a string representation of the cart's contents."""
        cart_contents = "\n".join([f"{quantity} x {product}" for product, quantity in self.items])
        return f"Cart:\n{cart_contents}\nTotal cost: {self.total_cost():.2f}"

    def __len__(self):
        """Returns the number of items in the cart."""
        return len(self.items)

    def __getitem__(self, index):
        """Returns the item at the specified index."""
        return self.items[index]

    def __iter__(self):
        """Returns an iterator for the items in the cart."""
        return CartIterator(self)

    def __iadd__(self, other):
        """Combines the contents of another cart with this cart."""
        if not isinstance(other, Cart):
            raise TypeError(f"Cannot combine Cart with {type(other).__name__}")
        self.items.extend(other.items)
        self.log(f"Combined cart with another cart containing {len(other)} items.")
        return self

class PaymentProcessor:
    """Base class for payment processing."""
    def pay(self, amount):
        """Processes the payment of the specified amount."""
        raise NotImplementedError("This method should be overridden by subclasses")

class CreditCardProcessor(PaymentProcessor, LoggingMixin):
    """Processes payments using a credit card."""
    def __init__(self, card_number, card_holder, expiration_date, cvv):
        self.card_number = self.validate_card_number()
        self.card_holder = self.validate_card_holder()
        self.expiration_date = self.validate_expiration_date()
        self.cvv = self.validate_cvv()

    def validate_card_number(self):
        """Validates the credit card number."""
        while True:
            card_number = input("Enter card number: ").strip()
            if re.fullmatch(r"\d{16}", card_number):
                return card_number
            print("Card number must be 16 digits.")

    def validate_card_holder(self):
        """Validates the card holder's name."""
        while True:
            card_holder = input("Enter card holder name: ").strip()
            if re.fullmatch(r"[A-Za-z\s]+", card_holder):
                return card_holder
            print("Card holder name must contain only letters and spaces.")

    def validate_expiration_date(self):
        """Validates the expiration date of the credit card."""
        while True:
            expiration_date = input("Enter expiration date (MM/YY): ").strip()
            if re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", expiration_date):
                current_year = int(datetime.now().strftime("%y"))
                current_month = int(datetime.now().strftime("%m"))
                exp_month, exp_year = map(int, expiration_date.split("/"))
                if exp_year > current_year or (exp_year == current_year and exp_month >= current_month):
                    return expiration_date
                print("The credit card is expired.")
            else:
                print("Expiration date must be in MM/YY format.")

    def validate_cvv(self):
        """Validates the CVV of the credit card."""
        while True:
            cvv = input("Enter CVV: ").strip()
            if re.fullmatch(r"\d{3,4}", cvv):
                return cvv
            print("CVV must be 3 or 4 digits.")

    def pay(self, amount):
        """Processes the payment using the credit card."""
        print(f"Processing credit card payment of ${amount:.2f}")
        print(f"Card Holder: {self.card_holder}")
        print(f"Card Number: {self.card_number}")
        print(f"Expiration Date: {self.expiration_date}")
        self.log(f"Processed payment of ${amount:.2f} using Credit Card ending in {self.card_number[-4:]}.")
        print("Payment successful!\n")

class PayPalProcessor(PaymentProcessor, LoggingMixin):
    """Processes payments using PayPal."""
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        """Processes the payment using PayPal."""
        print(f"Processing PayPal payment of ${amount:.2f}")
        print(f"PayPal Account: {self.email}")
        self.log(f"Processed payment of ${amount:.2f} using PayPal account {self.email}.")
        print("Payment successful!\n")

class BankTransferProcessor(PaymentProcessor, LoggingMixin):
    """Processes payments using a bank transfer."""
    def __init__(self, account_number, bank_name):
        self.account_number = account_number
        self.bank_name = bank_name

    def pay(self, amount):
        """Processes the payment using a bank transfer."""
        print(f"Processing bank transfer of ${amount:.2f}")
        print(f"Bank: {self.bank_name}")
        print(f"Account Number: {self.account_number}")
        self.log(f"Processed bank transfer of ${amount:.2f} to account {self.account_number} at {self.bank_name}.")
        print("Payment successful!\n")

# Пример использования
try:
    cart = Cart()
    product1 = Product("Laptop", 1200.00, "A powerful laptop")
    product2 = Product("Headphones", 200.00, "Noise-cancelling headphones")
    cart.add_product(product1, 1)
    cart.add_product(product2, 2)

    print("\nBefore applying discount:")
    print(cart)

    discount_choice = input("Choose discount type (percentage/fixed): ").strip().lower()
    if discount_choice == "percentage":
        discount_value = float(input("Enter percentage discount: "))
        discount = PercentageDiscount(discount_value)
    elif discount_choice == "fixed":
        discount_value = float(input("Enter fixed amount discount: "))
        discount = FixedAmountDiscount(discount_value)
    else:
        print("Invalid discount choice.")
        discount = None

    if discount:
        cart.apply_discount(discount)

    print("\nAfter applying discount:")
    print(cart)

    payment_method = input("Choose payment method (creditcard/paypal/banktransfer): ").strip().lower()
    if payment_method == "creditcard":
        payment_processor = CreditCardProcessor("4111111111111111", "John Doe", "12/25", "123")
    elif payment_method == "paypal":
        payment_processor = PayPalProcessor("user@example.com")
    elif payment_method == "banktransfer":
        payment_processor = BankTransferProcessor("123456789", "MyBank")
    else:
        print("Invalid payment method.")
        payment_processor = None

    if payment_processor:
        cart.pay(payment_processor)
except (InvalidPriceError, InvalidQuantityError, InvalidCardDetailsError) as e:
    print(f"Error: {e}")
