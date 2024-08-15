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
        """
        # Логирование в консоль
        print(f"LOG: {message}")

        # Если нужно логировать в файл, можно использовать следующий код:
        # with open("log.txt", "a") as log_file:
        #     log_file.write(f"{message}\n")


class InvalidPriceError(Exception):
    """
    Custom exception raised when an invalid price (negative or zero) is set for a product.
    """
    def __init__(self, price):
        """
        Initializes the InvalidPriceError with a specific price.

        Args:
            price: The invalid price that triggered the exception.
        """
        super().__init__(f"Invalid price: {price}. Price must be greater than 0.")


class InvalidQuantityError(Exception):
    """
    Custom exception raised when an invalid quantity (negative or zero) is added to the cart.
    """
    def __init__(self, quantity):
        """
        Initializes the InvalidQuantityError with a specific quantity.

        Args:
            quantity: The invalid quantity that triggered the exception.
        """
        super().__init__(f"Invalid quantity: {quantity}. Quantity must be greater than 0.")


class InvalidCardDetailsError(Exception):
    """Custom exception for invalid card details."""
    def __init__(self, message):
        super().__init__(f"Invalid card details: {message}")


class Product(LoggingMixin):
    """
    Represents a product in the store.

    Attributes:
        name: A string representing the name of the product.
        price: A float representing the price of the product.
        description: A string representing the description of the product.
    """

    def __init__(self, name, price, description):
        """
        Initializes a new Product instance.

        Args:
            name: The name of the product.
            price: The price of the product.
            description: The description of the product.

        Raises:
            InvalidPriceError: If the price is negative or zero.
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
            A string that describes the product.
        """
        return f"Product(name='{self.name}', price={self.price:.2f}, description='{self.description}')"

    def update_price(self, new_price):
        """
        Updates the price of the product.

        Args:
            new_price: The new price to set.

        Raises:
            InvalidPriceError: If the new price is negative or zero.
        """
        if new_price <= 0:
            raise InvalidPriceError(new_price)
        self.log(f"Price for {self.name} updated from {self.price:.2f} to {new_price:.2f}")
        self.price = new_price


class Discount:
    """
    Base class for discounts.

    Methods:
        apply: Applies the discount to a price. Should be overridden in subclasses.
    """

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


class PercentageDiscount(Discount, LoggingMixin):
    """
    Represents a percentage-based discount.

    Attributes:
        percentage: A float representing the percentage of the discount.
    """

    def __init__(self, percentage):
        """
        Initializes a new PercentageDiscount instance.

        Args:
            percentage: The percentage of the discount.
        """
        self.percentage = percentage

    def apply(self, price):
        """
        Applies the percentage discount to the given price.

        Args:
            price: The original price before the discount.

        Returns:
            The price after the percentage discount is applied.
        """
        discount_amount = price * (self.percentage / 100)
        new_price = price - discount_amount
        self.log(f"Applied {self.percentage}% discount: Old Price: {price:.2f}, New Price: {new_price:.2f}")
        return new_price


class FixedAmountDiscount(Discount, LoggingMixin):
    """
    Represents a fixed amount discount.

    Attributes:
        amount: A float representing the fixed discount amount.
    """

    def __init__(self, amount):
        """
        Initializes a new FixedAmountDiscount instance.

        Args:
            amount: The fixed discount amount.
        """
        self.amount = amount

    def apply(self, price):
        """
        Applies the fixed discount amount to the given price.

        Args:
            price: The original price before the discount.

        Returns:
            The price after the fixed amount discount is applied.
        """
        new_price = max(0, price - self.amount)
        self.log(f"Applied fixed discount: {self.amount:.2f}, Old Price: {price:.2f}, New Price: {new_price:.2f}")
        return new_price


class DiscountMixin:
    """
    Mixin class to apply discounts to all products in the cart.

    Methods:
        apply_discount: Applies a given discount to all products in the cart.
    """

    def apply_discount(self, discount: Discount):
        """
        Applies the given discount to each product in the cart.

        Args:
            discount: An instance of Discount to be applied to each product.
        """
        for i, (product, quantity) in enumerate(self.items):
            discounted_price = discount.apply(product.price)
            self.items[i] = (Product(product.name, discounted_price, product.description), quantity)
        self.log(f"Discount applied to all products in the cart using {discount.__class__.__name__}.")


class Cart(DiscountMixin, LoggingMixin):
    """
    Represents a shopping cart that holds products and handles payments.

    Attributes:
        items: A list of tuples where each tuple contains a product and its quantity.
    """

    def __init__(self):
        """Initializes an empty shopping cart."""
        self.items = []
        self.log("Initialized an empty shopping cart.")

    def add_product(self, product, quantity):
        """
        Adds a product and its quantity to the cart.

        Args:
            product: An instance of Product to add to the cart.
            quantity: The quantity of the product to add.

        Raises:
            InvalidQuantityError: If the quantity is negative or zero.
        """
        if quantity <= 0:
            raise InvalidQuantityError(quantity)
        self.items.append((product, quantity))
        self.log(f"Added product: {product.name}, Quantity: {quantity} to the cart.")

    def total_cost(self):
        """
        Calculates the total cost of all products in the cart.

        Returns:
            The total cost as a float.
        """
        total = sum(product.price * quantity for product, quantity in self.items)
        self.log(f"Total cost calculated: {total:.2f}")
        return total

    def pay(self, payment_processor):
        """
        Processes payment for the total cost of the cart.

        Args:
            payment_processor: An instance of a PaymentProcessor to handle the payment.
        """
        total = self.total_cost()
        payment_processor.pay(total)
        self.log(f"Payment of ${total:.2f} processed using {payment_processor.__class__.__name__}.")

    def __str__(self):
        """
        Returns a string representation of the cart contents and total cost.

        Returns:
            A string that lists all items in the cart and their total cost.
        """
        cart_contents = "\n".join([f"{quantity} x {product}" for product, quantity in self.items])
        return f"Cart:\n{cart_contents}\nTotal cost: {self.total_cost():.2f}"


class PaymentProcessor:
    """
    Base class for payment processing.

    Methods:
        pay: Processes a payment. Should be overridden in subclasses.
    """

    def pay(self, amount):
        """
        Processes a payment of the given amount.

        Args:
            amount: The total amount to be paid.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class CreditCardProcessor(PaymentProcessor, LoggingMixin):
    """
    Processes payments using a credit card.

    Attributes:
        card_number: A string representing the credit card number.
        card_holder: A string representing the name of the card holder.
        expiration_date: A string representing the expiration date of the card.
        cvv: A string representing the CVV code of the card.
    """

    def __init__(self, card_number, card_holder, expiration_date, cvv):
        """
        Initializes a new CreditCardProcessor instance.

        Args:
            card_number: The credit card number.
            card_holder: The name of the card holder.
            expiration_date: The expiration date of the card.
            cvv: The CVV code of the card.

        Raises:
            InvalidCardDetailsError: If any card details are invalid.
        """
        self.validate_card_details(card_number, card_holder, expiration_date, cvv)
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiration_date = expiration_date
        self.cvv = cvv

    def validate_card_details(self, card_number, card_holder, expiration_date, cvv):
        """
        Validates the credit card details.

        Args:
            card_number: The credit card number.
            card_holder: The name of the card holder.
            expiration_date: The expiration date of the card.
            cvv: The CVV code of the card.

        Raises:
            InvalidCardDetailsError: If any of the card details are invalid.
        """
        if not re.fullmatch(r"\d{16}", card_number):
            raise InvalidCardDetailsError("Card number must be 16 digits.")

        if not re.fullmatch(r"[A-Za-z\s]+", card_holder):
            raise InvalidCardDetailsError("Card holder name must contain only letters and spaces.")

        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", expiration_date):
            raise InvalidCardDetailsError("Expiration date must be in MM/YY format.")

        # Check if the card is expired
        current_year = int(datetime.now().strftime("%y"))
        current_month = int(datetime.now().strftime("%m"))
        exp_month, exp_year = map(int, expiration_date.split("/"))
        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            raise InvalidCardDetailsError("The credit card is expired.")

        if not re.fullmatch(r"\d{3,4}", cvv):
            raise InvalidCardDetailsError("CVV must be 3 or 4 digits.")

    def pay(self, amount):
        """
        Processes the payment using the credit card.

        Args:
            amount: The total amount to be paid.

        Returns:
            None
        """
        print(f"Processing credit card payment of ${amount:.2f}")
        print(f"Card Holder: {self.card_holder}")
        print(f"Card Number: {self.card_number}")
        print(f"Expiration Date: {self.expiration_date}")
        self.log(f"Processed payment of ${amount:.2f} using Credit Card ending in {self.card_number[-4:]}.")
        print("Payment successful!\n")


class PayPalProcessor(PaymentProcessor, LoggingMixin):
    """
    Processes payments using PayPal.

    Attributes:
        email: A string representing the PayPal account email.
    """

    def __init__(self, email):
        """
        Initializes a new PayPalProcessor instance.

        Args:
            email: The PayPal account email.
        """
        self.email = email

    def pay(self, amount):
        """
        Processes the payment using PayPal.

        Args:
            amount: The total amount to be paid.

        Returns:
            None
        """
        print(f"Processing PayPal payment of ${amount:.2f}")
        print(f"PayPal Account: {self.email}")
        self.log(f"Processed payment of ${amount:.2f} using PayPal account {self.email}.")
        print("Payment successful!\n")


class BankTransferProcessor(PaymentProcessor, LoggingMixin):
    """
    Processes payments using a bank transfer.

    Attributes:
        bank_account: A string representing the bank account number.
        bank_name: A string representing the name of the bank.
    """

    def __init__(self, bank_account, bank_name):
        """
        Initializes a new BankTransferProcessor instance.

        Args:
            bank_account: The bank account number.
            bank_name: The name of the bank.
        """
        self.bank_account = bank_account
        self.bank_name = bank_name

    def pay(self, amount):
        """
        Processes the payment using a bank transfer.

        Args:
            amount: The total amount to be paid.

        Returns:
            None
        """
        print(f"Processing bank transfer of ${amount:.2f}")
        print(f"Bank Name: {self.bank_name}")
        print(f"Bank Account: {self.bank_account}")
        self.log(f"Processed payment of ${amount:.2f} using bank transfer to account {self.bank_account}.")
        print("Payment successful!\n")


# Example usage

try:
    # Create several products with valid and invalid prices
    """
    Creates instances of the Product class for each item, testing both valid and invalid prices.

    Args:
        product1: An instance of Product representing a valid laptop product.
        product2: An instance of Product representing a valid smartphone product.
        product3: An instance of Product representing a valid headphones product.
        product_invalid: An instance of Product with an invalid price (should raise InvalidPriceError).

    Returns:
        None
    """
    product1 = Product("Laptop", 1200.99, "A high-performance laptop")
    product2 = Product("Smartphone", 699.99, "A latest model smartphone")
    product3 = Product("Headphones", 199.99, "Noise-cancelling headphones")

    # Example of invalid product creation (should raise an exception)
    try:
        product_invalid = Product("Invalid Product", -50, "This should fail")
    except InvalidPriceError as e:
        print(e)

    # Create a cart and add products to it, including testing invalid quantities
    """
    Initializes a Cart object and adds products to it with specified quantities,
    including a test for invalid quantity (should raise InvalidQuantityError).

    Args:
        cart: An instance of Cart to which products are added.
        product1: The product representing a laptop is added with quantity 1.
        product2: The product representing a smartphone is added with quantity 2.
        product3: The product representing headphones is added with quantity 3.
        invalid_quantity_test: Attempts to add a product with an invalid quantity (should raise InvalidQuantityError).

    Returns:
        None
    """
    cart = Cart()
    cart.add_product(product1, 1)
    cart.add_product(product2, 2)
    cart.add_product(product3, 3)

    # Example of invalid quantity addition (should raise an exception)
    try:
        cart.add_product(product1, -1)
    except InvalidQuantityError as e:
        print(e)

    # Display cart contents before applying any discounts
    """
    Prints the contents of the cart and the total cost before any discounts are applied.

    Args:
        cart: The Cart instance whose contents are displayed.

    Returns:
        None
    """
    print("Before applying discount:")
    print(cart)

    # Apply discount based on user choice
    """
    Prompts the user to choose a discount type (percentage or fixed) and applies it to the cart.

    Args:
        discount_choice: A string input from the user indicating the discount type.
        percentage: A float representing the percentage discount, if chosen.
        amount: A float representing the fixed amount discount, if chosen.
        discount: An instance of Discount (either PercentageDiscount or FixedAmountDiscount).

    Returns:
        None
    """
    discount_choice = input("Choose discount type (percentage/fixed): ").strip().lower()

    if discount_choice in ["percentage", "fixed"]:
        if discount_choice == "percentage":
            percentage = float(input("Enter discount percentage: "))
            if percentage > 100:
                print("Discount percentage cannot exceed 100%. No discount applied.")
                discount = None
            else:
                discount = PercentageDiscount(percentage)
        elif discount_choice == "fixed":
            amount = float(input("Enter discount amount: "))
            discount = FixedAmountDiscount(amount)
    else:
        try:
            # Try to interpret the input as a percentage
            percentage = float(discount_choice)
            if percentage > 100:
                print("Discount percentage cannot exceed 100%. No discount applied.")
                discount = None
            else:
                discount = PercentageDiscount(percentage)
        except ValueError:
            discount = None
            print("No discount applied.")

    if discount:
        cart.apply_discount(discount)

    # Display cart contents after applying the discount
    """
    Prints the contents of the cart and the total cost after the discount has been applied.

    Args:
        cart: The Cart instance whose contents are displayed after the discount.

    Returns:
        None
    """
    print("After applying discount:")
    print(cart)

    # Payment process
    """
    Prompts the user to choose a payment method and processes the payment.

    Args:
        choice: A string input from the user indicating the chosen payment method.
        processor: An instance of PaymentProcessor (either CreditCardProcessor, PayPalProcessor, or BankTransferProcessor).

    Returns:
        None
    """
    print("Choose payment method:")
    print("1. Credit Card")
    print("2. PayPal")
    print("3. Bank Transfer")

    choice = input("Enter the number or name of the payment method: ").strip().lower()

    if choice in ['1', 'credit card']:
        card_number = input("Enter card number: ").strip()
        card_holder = input("Enter card holder name: ").strip()
        expiration_date = input("Enter expiration date (MM/YY): ").strip()
        cvv = input("Enter CVV: ").strip()
        processor = CreditCardProcessor(card_number, card_holder, expiration_date, cvv)
    elif choice in ['2', 'paypal']:
        email = input("Enter PayPal email: ").strip()
        processor = PayPalProcessor(email)
    elif choice in ['3', 'bank transfer']:
        bank_account = input("Enter bank account number: ").strip()
        bank_name = input("Enter bank name: ").strip()
        processor = BankTransferProcessor(bank_account, bank_name)
    else:
        print("Invalid payment method selected.")
        processor = None

    # Execute payment if a valid processor was selected
    """
    Executes the payment using the selected payment processor.

    Args:
        processor: The PaymentProcessor instance used to process the payment.

    Returns:
        None
    """
    if processor:
        cart.pay(processor)

except (InvalidPriceError, InvalidQuantityError, InvalidCardDetailsError) as e:
    print(e)
