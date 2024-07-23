def mutual_friends(user1, user2, friendships):
    if user1 not in friendships or user2 not in friendships:
        return set()  # Return an empty set if either user is not in the dictionary
    return friendships[user1] & friendships[user2]

# Example friendships data
friendships = {
    "user1": {"user2", "user3", "user4"},
    "user2": {"user1", "user3"},
    "user3": {"user1", "user2", "user4"},
    "user4": {"user1", "user3"}
}

# Get user input
user1 = input("Enter the first user: ")
user2 = input("Enter the second user: ")

# Calculate and print mutual friends
mutual = mutual_friends(user1, user2, friendships)
print(f"Mutual friends between {user1} and {user2}: {mutual}")
