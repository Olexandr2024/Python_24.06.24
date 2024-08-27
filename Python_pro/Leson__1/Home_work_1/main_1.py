import re
from datetime import datetime


class LoggingMixin:
    """
    Mixin class to provide logging functionality for actions in Product and Cart classes.
    """

    def log(self, message):
        """
        Logs a message to the console or a file.

        Args:
            message: A string message describing the action to log.

        This method is intended to provide basic logging functionality.
        It can be overridden or extended in subclasses to implement
        more sophisticated logging mechanisms, such as writing to a log file
        or integrating with external logging systems.
        """
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
        """
        Initializes a new product with the given name, price, and description.

        Args:
            name (str): The name of the product.
            price (float): The price of the product. Must be greater than 0.
            description (str): A brief description of the product.

        Raises:
            InvalidPriceError: If the price is not greater than 0.
        """
        if price <= 0:
            raise InvalidPriceError(price)
        self.name = name
        self.price = price
        self.description = description
        self.log(f"Created product: {self.name}, Price: {self.price:.2f}")

    def __str__(self):
        """
        Returns a string representation of the product.

        Returns:
            str: A string describing the product.
        """
        return f"Product(name='{self.name}', price={self.price:.2f}, description='{self.description}')"

    def update_price(self, new_price):
        """
        Updates the price of the product.

        Args:
            new_price (float): The new price of the product. Must be greater than 0.

        Raises:
            InvalidPriceError: If the new price is not greater than 0.
        """
        if new_price <= 0:
            raise InvalidPriceError(new_price)
        self.log(f"Price for {self.name} updated from {self.price:.2f} to {new_price:.2f}")
        self.price = new_price


class Discount:
    """Base class for discounts."""

    def apply(self, price):
        """
        Applies the discount to the given price.

        Args:
            price (float): The original price to which the discount will be applied.

        Returns:
            float: The price after the discount is applied.

        Raises:
            NotImplementedError: This method should be overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class PercentageDiscount(Discount, LoggingMixin):
    """Applies a percentage discount to a price."""

    def __init__(self, percentage):
        """
        Initializes the percentage discount.

        Args:
            percentage (float): The percentage discount to apply.
        """
        self.percentage = percentage

    def apply(self, price):
        """
        Applies the percentage discount to the given price.

        Args:
            price (float): The original price to which the discount will be applied.

        Returns:
            float: The price after the discount is applied.
        """
        discount_amount = price * (self.percentage / 100)
        new_price = price - discount_amount
        self.log(f"Applied {self.percentage}% discount: Old Price: {price:.2f}, New Price: {new_price:.2f}")
        return new_price


class FixedAmountDiscount(Discount, LoggingMixin):
    """Applies a fixed amount discount to a price."""

    def __init__(self, amount):
        """
        Initializes the fixed amount discount.

        Args:
            amount (float): The fixed amount discount to apply.
        """
        self.amount = amount

    def apply(self, price):
        """
        Applies the fixed amount discount to the given price.

        Args:
            price (float): The original price to which the discount will be applied.

        Returns:
            float: The price after the discount is applied. Ensures the price does not go below zero.
        """
        new_price = max(0, price - self.amount)
        self.log(f"Applied fixed discount: {self.amount:.2f}, Old Price: {price:.2f}, New Price: {new_price:.2f}")
        return new_price


class DiscountMixin:
    """Mixin class to apply discounts to all products in the cart."""

    def apply_discount(self, discount: Discount):
        """
        Applies a given discount to all products in the cart.

        Args:
            discount (Discount): The discount to apply to the products in the cart.
        """
        for i, (product, quantity) in enumerate(self.items):
            discounted_price = discount.apply(product.price)
            self.items[i] = (Product(product.name, discounted_price, product.description), quantity)
        self.log(f"Discount applied to all products in the cart using {discount.__class__.__name__}.")


class Cart(DiscountMixin, LoggingMixin):
    """Represents a shopping cart that holds products and handles payments."""

    def __init__(self):
        """
        Initializes an empty shopping cart.
        """
        self.items = []
        self.log("Initialized an empty shopping cart.")

    def add_product(self, product, quantity):
        """
        Adds a product and its quantity to the cart.

        Args:
            product (Product): The product to add to the cart.
            quantity (int): The quantity of the product to add. Must be greater than 0.

        Raises:
            InvalidQuantityError: If the quantity is not greater than 0.
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        self.items.append((product, quantity))
        self.log(f"Added product: {product.name}, Quantity: {quantity} to the cart.")

    def total_cost(self):
        """
        Calculates the total cost of all items in the cart.

        Returns:
            float: The total cost of the items in the cart.
        """
        total = sum(product.price * quantity for product, quantity in self.items)
        self.log(f"Total cost calculated: {total:.2f}")
        return total

    def pay(self, payment_processor):
        """
        Processes the payment for the total cost of the cart.

        Args:
            payment_processor (PaymentProcessor): The payment processor to use for the transaction.
        """
        total = self.total_cost()
        payment_processor.pay(total)
        self.log(f"Payment of ${total:.2f} processed using {payment_processor.__class__.__name__}.")

    def __str__(self):
        """
        Returns a string representation of the cart's contents and total cost.

        Returns:
            str: A string describing the contents of the cart and the total cost.
        """
        cart_contents = "\n".join([f"{quantity} x {product}" for product, quantity in self.items])
        return f"Cart:\n{cart_contents}\nTotal cost: {self.total_cost():.2f}"

    def __len__(self):
        """
        Returns the number of items in the cart.

        Returns:
            int: The number of items in the cart.
        """
        return len(self.items)

    def __getitem__(self, index):
        """
        Allows access to items in the cart by index.

        Args:
            index (int): The index of the item to access.

        Returns:
            tuple: A tuple containing the product and quantity at the specified index.
        """
        return self.items[index]

    def __iter__(self):
        """
        Returns an iterator for the cart items.

        Returns:
            iterator: An iterator for the cart items.
        """
        return iter(self.items)

    def __iadd__(self, other):
        """
        Combines another cart with this cart using the += operator.

        Args:
            other (Cart): Another cart whose items will be added to this cart.

        Returns:
            Cart: The combined cart.
        """
        if not isinstance(other, Cart):
            raise TypeError(f"Cannot combine Cart with {type(other).__name__}")
        self.items.extend(other.items)
        self.log(f"Combined cart with another cart containing {len(other)} items.")
        return self


class PaymentProcessor:
    """Base class for payment processing."""

    def pay(self, amount):
        """
        Processes a payment for the given amount.

        Args:
            amount (float): The amount to be paid.

        Raises:
            NotImplementedError: This method should be overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class CreditCardProcessor(PaymentProcessor, LoggingMixin):
    """Processes payments using a credit card."""

    def __init__(self, card_number, card_holder, expiration_date, cvv):
        """
        Initializes the credit card processor with card details.

        Args:
            card_number (str): The credit card number.
            card_holder (str): The name of the card holder.
            expiration_date (str): The expiration date of the card (MM/YY).
            cvv (str): The CVV code of the card.

        Raises:
            InvalidCardDetailsError: If any card details are invalid.
        """
        self.card_number = self.validate_card_number()
        self.card_holder = self.validate_card_holder()
        self.expiration_date = self.validate_expiration_date()
        self.cvv = self.validate_cvv()

    def validate_card_number(self):
        """
        Validates the credit card number.

        Returns:
            str: The validated card number.

        Raises:
            InvalidCardDetailsError: If the card number is not 16 digits.
        """
        while True:
            card_number = input("Enter card number: ").strip()
            if re.fullmatch(r"\d{16}", card_number):
                return card_number
            print("Card number must be 16 digits.")

    def validate_card_holder(self):
        """
        Validates the card holder's name.

        Returns:
            str: The validated card holder's name.

        Raises:
            InvalidCardDetailsError: If the card holder's name contains invalid characters.
        """
        while True:
            card_holder = input("Enter card holder name: ").strip()
            if re.fullmatch(r"[A-Za-z\s]+", card_holder):
                return card_holder
            print("Card holder name must contain only letters and spaces.")

    def validate_expiration_date(self):
        """
        Validates the expiration date of the card.

        Returns:
            str: The validated expiration date.

        Raises:
            InvalidCardDetailsError: If the expiration date is not valid or the card is expired.
        """
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
        """
        Validates the CVV code of the card.

        Returns:
            str: The validated CVV code.

        Raises:
            InvalidCardDetailsError: If the CVV code is not 3 or 4 digits.
        """
        while True:
            cvv = input("Enter CVV: ").strip()
            if re.fullmatch(r"\d{3,4}", cvv):
                return cvv
            print("CVV must be 3 or 4 digits.")

    def pay(self, amount):
        """
        Processes the payment for the given amount using the credit card.

        Args:
            amount (float): The amount to be paid.
        """
        print(f"Processing credit card payment of ${amount:.2f}")
        print(f"Card Holder: {self.card_holder}")
        print(f"Card Number: {self.card_number}")
        print(f"Expiration Date: {self.expiration_date}")
        self.log(f"Processed payment of ${amount:.2f} using Credit Card ending in {self.card_number[-4:]}.")
        print("Payment successful!\n")


class PayPalProcessor(PaymentProcessor, LoggingMixin):
    """Processes payments using PayPal."""

    def __init__(self, email):
        """
        Initializes the PayPal processor with the user's email.

        Args:
            email (str): The email associated with the PayPal account.
        """
        self.email = email

    def pay(self, amount):
        """
        Processes the payment for the given amount using PayPal.

        Args:
            amount (float): The amount to be paid.
        """
        print(f"Processing PayPal payment of ${amount:.2f}")
        print(f"PayPal Account: {self.email}")
        self.log(f"Processed payment of ${amount:.2f} using PayPal account {self.email}.")
        print("Payment successful!\n")


class BankTransferProcessor(PaymentProcessor, LoggingMixin):
    """Processes payments using a bank transfer."""

    def __init__(self, bank_account, bank_name):
        """
        Initializes the bank transfer processor with bank details.

        Args:
            bank_account (str): The bank account number.
            bank_name (str): The name of the bank.
        """
        self.bank_account = bank_account
        self.bank_name = bank_name

    def pay(self, amount):
        """
        Processes the payment for the given amount using a bank transfer.

        Args:
            amount (float): The amount to be paid.
        """
        print(f"Processing bank transfer of ${amount:.2f}")
        print(f"Bank Name: {self.bank_name}")
        print(f"Bank Account: {self.bank_account}")
        self.log(f"Processed payment of ${amount:.2f} using bank transfer to account {self.bank_account}.")
        print("Payment successful!\n")


# Example usage

try:
    """
    Creates three products with a name, price, and description.
    """
    product1 = Product("Laptop", 1200.99, "A high-performance laptop")
    product2 = Product("Smartphone", 699.99, "A latest model smartphone")
    product3 = Product("Headphones", 199.99, "Noise-cancelling headphones")

    """
    Creates a cart and adds products to it.
    """
    cart = Cart()
    cart.add_product(product1, 1)  # Adds one laptop to the cart
    cart.add_product(product2, 2)  # Adds two smartphones to the cart
    cart.add_product(product3, 3)  # Adds three headphones to the cart

    """
    Prints the contents of the cart before applying any discount.
    """
    print("Before applying discount:")
    print(cart)

    """
    Prompts the user to choose a discount type: percentage or fixed.
    """
    discount_choice = input("Choose discount type (percentage/fixed): ").strip().lower()

    if discount_choice in ["percentage", "fixed"]:
        if discount_choice == "percentage":
            """
            If percentage discount is chosen, prompts the user for the discount percentage.
            """
            percentage = float(input("Enter discount percentage: "))
            if percentage > 100:
                """
                Ensures the discount percentage does not exceed 100%.
                """
                print("Discount percentage cannot exceed 100%. No discount applied.")
                discount = None
            else:
                discount = PercentageDiscount(percentage)  # Applies percentage discount
        elif discount_choice == "fixed":
            """
            If fixed discount is chosen, prompts the user for the discount amount.
            """
            amount = float(input("Enter discount amount: "))
            discount = FixedAmountDiscount(amount)  # Applies fixed discount
    else:
        try:
            """
            Allows for direct input of a discount percentage by the user.
            """
            percentage = float(discount_choice)
            if percentage > 100:
                print("Discount percentage cannot exceed 100%. No discount applied.")
                discount = None
            else:
                discount = PercentageDiscount(percentage)
        except ValueError:
            """
            If an invalid value is entered, no discount is applied.
            """
            discount = None
            print("No discount applied.")

    """
    Applies the discount to all products in the cart, if applicable.
    """
    if discount:
        cart.apply_discount(discount)

    """
    Prints the contents of the cart after applying the discount.
    """
    print("After applying discount:")
    print(cart)

    """
    Prompts the user to choose a payment method.
    """
    print("Choose payment method:")
    print("1. Credit Card")
    print("2. PayPal")
    print("3. Bank Transfer")

    """
    Gets the user's choice and creates the corresponding payment processor.
    """
    choice = input("Enter the number or name of the payment method: ").strip().lower()

    if choice in ['1', 'credit card']:
        """
        Uses credit card as the payment method.
        """
        processor = CreditCardProcessor(None, None, None, None)
    elif choice in ['2', 'paypal']:
        """
        Uses PayPal as the payment method.
        """
        email = input("Enter PayPal email: ").strip()
        processor = PayPalProcessor(email)
    elif choice in ['3', 'bank transfer']:
        """
        Uses bank transfer as the payment method.
        """
        bank_account = input("Enter bank account number: ").strip()
        bank_name = input("Enter bank name: ").strip()
        processor = BankTransferProcessor(bank_account, bank_name)
    else:
        """
        Handles invalid payment method selection.
        """
        print("Invalid payment method selected.")
        processor = None

    """
    Processes the payment using the selected payment method, if valid.
    """
    if processor:
        cart.pay(processor)

except (InvalidPriceError, InvalidQuantityError, InvalidCardDetailsError) as e:
    """
    Handles exceptions that may arise during product creation or payment.
    """
    print(e)
