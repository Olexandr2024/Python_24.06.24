class CreditCardProcessor(PaymentProcessor, LoggingMixin):
    """Processes payments using a credit card."""
    def __init__(self, card_number, card_holder, expiration_date, cvv):
        self.card_number = self.validate_card_number_format(card_number)
        self.card_holder = self.validate_card_holder(card_holder)
        self.expiration_date = self.validate_expiration_date(expiration_date)
        self.cvv = self.validate_cvv(cvv)

    def validate_card_number_format(self, card_number):
        """Validates the format of the credit card number (9999-9999-9999-9999)."""
        if re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{4}", card_number):
            return card_number
        else:
            raise InvalidCardDetailsError("Card number must be in the format 9999-9999-9999-9999.")

    # Інші методи залишаються без змін
