class ArithmeticSequence:
    def __init__(self, start, difference):
        self.start = start
        self.difference = difference

    def __getitem__(self, n):
        if n < 0:
            raise IndexError("Index must be non-negative")
        return self.start + n * self.difference

    def __iter__(self):
        value = self.start
        while True:
            yield value
            value += self.difference

# Пример использования:
seq = ArithmeticSequence(1, 3)
print(seq[0])  # 1
print(seq[1])  # 4
print(seq[5])  # 16

# Итерация по последовательности:
for i, value in enumerate(seq):
    if i >= 3:
        break
    print(value)