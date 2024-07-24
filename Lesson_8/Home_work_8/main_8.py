# Task_1
def are_elements_unique(lst):
    return len(lst) == len(set(lst))

lst1 = [1, 2, 3, 4, 5]
lst2 = [1, 2, 2, 3, 4, 5]

print(f"All  are unique: {are_elements_unique(lst1)}")
print(f"All lst2 are unique: {are_elements_unique(lst2)}")

# Task_2
def count_unique_elements(lst):
    frequency = {}
    for item in lst:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1

    unique_count = sum(1 for item in frequency if frequency[item] == 1)
    return unique_count

lst = [1, 2, 2, 3, 4, 5, 5, 5, 6]

unique_count = count_unique_elements(lst)
print(f"The number of unique elements in the list: {unique_count}")

# Task_3
def has_unique_values(dct):
    values = list(dct.values())
    return len(values) == len(set(values))

# Example usage
dct = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 2
}

if has_unique_values(dct):
    print("All values in the dictionary are unique.")
else:
    print("There are duplicate values in the dictionary.")

# Task_4
def mutual_friends(user1, user2, friendships):
    if user1 not in friendships or user2 not in friendships:
        return set()
    return friendships[user1] & friendships[user2]


friendships = {
    "user1": {"user2", "user3", "user4"},
    "user2": {"user1", "user3"},
    "user3": {"user1", "user2", "user4"},
    "user4": {"user1", "user3"}
}


user1 = input("Enter the first user: ")
user2 = input("Enter the second user: ")


mutual = mutual_friends(user1, user2, friendships)
print(f"Mutual friends between {user1} and {user2}: {mutual}")

# Task_5
def find_longest_common_word(str1, str2):
    words1 = set(str1.split())
    words2 = set(str2.split())

    common_words = words1 & words2

    if not common_words:
        return None

    longest_word = max(common_words, key=len)
    return longest_word



str1 = input("Enter the first string: ")
str2 = input("Enter the second string: ")


result = find_longest_common_word(str1, str2)
if result:
    print(f"The longest common word is: {result}")
else:
    print("No common words found")

