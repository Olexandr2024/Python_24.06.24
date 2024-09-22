# Task 1

import re


text = "Rbr rBBR RbR"


pattern = r'[Rr][Bb]+[Rr]'


matches = re.findall(pattern, text)

print(matches)

# Task 3
import re

def validate_email(email: str) -> bool:
    """
    Validates an email string based on specific rules.

    The function checks whether the input email adheres to the following criteria:
    - Contains digits (0-9).
    - Uses only Latin letters (both uppercase A-Z and lowercase a-z).
    - The body of the email may contain the characters "_" and "-", but they cannot be the first character.
    - The "-" character cannot repeat consecutively.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email matches the specified pattern, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9]+[a-zA-Z0-9_-]*[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(pattern, email):
        # Ensure that the '-' does not repeat consecutively in the email body
        if '--' not in email:
            return True
    return False

# Task 4
def validate_login(login):
    """Validates the login string."""
    if 2 <= len(login) <= 10 and re.fullmatch(r"[A-Za-z0-9]+", login):
        return login
    else:
        raise ValueError("Login must be 2 to 10 characters long and contain only letters and digits.")
try:
    user_login = validate_login("user123")
    print(f"Valid login: {user_login}")
except ValueError as e:
    print(f"Error: {e}")
