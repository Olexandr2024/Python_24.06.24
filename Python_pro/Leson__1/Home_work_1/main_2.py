from math import gcd

class ProperFraction:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator
        self._simplify()

    def _simplify(self):
        divisor = gcd(self.numerator, self.denominator)
        self.numerator //= divisor
        self.denominator //= divisor

    def __add__(self, other):
        return ProperFraction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator
        )

    def __sub__(self, other):
        return ProperFraction(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator
        )

    def __mul__(self, other):
        return ProperFraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )

    def __eq__(self, other):
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __lt__(self, other):
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"


a = ProperFraction(1, 2)
b = ProperFraction(3, 4)

print(a + b)  # 5/4
print(a - b)  # -1/4
print(a * b)  # 3/8
print(a == b)  # False
print(a < b)  # True
