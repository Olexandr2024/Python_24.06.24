class ArithmeticSequence:
    def __init__(self, start, difference):
        self.start = start
        self.difference = difference

    def __getitem__(self, n):
        if n < 0:
            raise IndexError("Index must be non-negative")
        return self.start + n * self.difference

