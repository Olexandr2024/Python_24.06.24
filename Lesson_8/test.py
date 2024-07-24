def count_unique_elements(lst):
    # Создаем словарь для хранения частоты каждого элемента
    frequency = {}
    for item in lst:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1

    # Подсчитываем количество элементов, которые встречаются только один раз
    unique_count = sum(1 for item in frequency if frequency[item] == 1)
    return unique_count

# Пример списка
lst = [1, 2, 2, 3, 4, 5, 5, 5, 6]

# Подсчет уникальных элементов
unique_count = count_unique_elements(lst)
print(f"The number of unique elements in the list: {unique_count}")
