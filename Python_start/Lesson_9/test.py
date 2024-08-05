def number_to_words(n):
    to_19 = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
    tens = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()

    def get_words(num):
        if num < 20:
            return to_19[num]
        elif num < 100:
            return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + to_19[num % 10])
        else:
            return to_19[num // 100] + ' hundred' + (' ' + get_words(num % 100) if num % 100 else '')

    return get_words(int(n))

def dollars_and_cents_to_words(amount):
    dollars, cents = amount.split(',')
    return f"{number_to_words(dollars)} dollars and {number_to_words(cents)} cents"

# Пример использования
amount = input("Enter the amount in the format dollars,cents (e.g.,): ")
print(dollars_and_cents_to_words(amount))
