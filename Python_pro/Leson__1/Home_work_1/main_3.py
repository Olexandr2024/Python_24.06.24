# lesson 6

# Task 1

def geometric_progression(start, ratio):
    """
        Generator function for rotating members of geometric progression.

        Argumenti:
            start (float): First member of the progression.
            ratio (float): The relationship between successive members.

        Turns:
            float: Advance term of geometric progression.
        """
    current = start
    while True:
        yield current
        current *= ratio
gp = geometric_progression(2, 3)
for _ in range(5):
    print(next(gp))

# Task 2
def my_range(start, stop=None, step=1):
    """
    Generator function that mimics the built-in range() function.

    Args:
        start (int): The starting value of the sequence, or if stop is not provided, the end value.
        stop (int, optional): The end value of the sequence (exclusive). If not provided, start is treated as the end.
        step (int, optional): The increment between each value in the sequence. Default is 1.

    Yields:
        int: The next value in the range sequence.
    """
    if stop is None:
        # If stop is not provided, treat start as stop and set start to 0
        stop = start
        start = 0

    if step == 0:
        raise ValueError("step must not be zero")

    # Check if the range can generate values based on the step direction
    if (step > 0 and start >= stop) or (step < 0 and start <= stop):
        return  # No values to generate

    current = start
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        yield current
        current += step
for i in my_range(1, 10, 2):
    print(i)

# Task 3

def prime_numbers(limit):
    """
    Generator function that yields prime numbers up to a given limit.

    Args:
        limit (int): The upper limit for generating prime numbers (exclusive).

    Yields:
        int: The next prime number in the sequence.
    """
    def is_prime(n):
        """Helper function to check if a number is prime."""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    for num in range(2, limit):
        if is_prime(num):
            yield num
for prime in prime_numbers(20):
    print(prime)

# Task 4

from datetime import datetime, timedelta

def date_range(start_date, end_date):
    """
    Generator function that yields dates from start_date to end_date (inclusive).

    Args:
        start_date (datetime): The starting date of the range.
        end_date (datetime): The ending date of the range.

    Yields:
        datetime: The next date in the sequence.
    """
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

start = datetime(2024, 9, 1)
end = datetime(2024, 9, 5)

for date in date_range(start, end):
    print(date.strftime('%Y-%m-%d'))

# lesson 7

# Task 1

def custom_sequence(func, first_value, n):
    """
    Generator function that yields values of a custom numerical sequence.

    Args:
        func (callable): A function that defines the law of the sequence.
        first_value (numeric): The first value of the sequence.
        n (int): The number of terms to generate.

    Yields:
        numeric: The next value in the sequence.

    The sequence stops when either the n-th term is generated,
    or a command to terminate is given (via StopIteration).
    """
    current_value = first_value
    for _ in range(n):
        yield current_value
        current_value = func(current_value)

def next_term(x):
    return x + 3


gen = custom_sequence(next_term, 2, 5)

for val in gen:
    print(val)

# Task 2

import time

def memoize_fibonacci():
    """
    Memoization closure for Fibonacci sequence.
    Returns a memoized Fibonacci function that stores previously computed results.
    """
    cache = {}  # Dictionary to store previously computed Fibonacci numbers

    def fibonacci(n):
        if n in cache:
            return cache[n]  # Return cached result if it exists
        if n <= 1:
            return n  # Base case: Fib(0) = 0, Fib(1) = 1
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)  # Compute and store in cache
        return cache[n]

    return fibonacci

# Memoized Fibonacci function
fib_memoized = memoize_fibonacci()

# Simple recursive Fibonacci (no memoization)
def fibonacci_recursive(n):
    """
    Simple recursive Fibonacci function without memoization.
    """
    if n <= 1:
        return n  # Base case: Fib(0) = 0, Fib(1) = 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# Compare execution speed
n = 35  # Compute the 35th Fibonacci number for comparison

# Test for memoized Fibonacci
start_time = time.time()
fib_memoized_result = fib_memoized(n)
memoized_time = time.time() - start_time
print(f"Memoized Fibonacci result: {fib_memoized_result} (Time: {memoized_time:.6f} seconds)")

# Test for simple recursive Fibonacci
start_time = time.time()
fib_recursive_result = fibonacci_recursive(n)
recursive_time = time.time() - start_time
print(f"Recursive Fibonacci result: {fib_recursive_result} (Time: {recursive_time:.6f} seconds)")

# Task 3

def apply_and_sum(numbers, user_function):
    """
    Applies a user-defined function to each element in the list of numbers
    and returns the sum of the transformed elements.

    :param numbers: List of numbers to process
    :param user_function: Function to apply to each element of the list
    :return: Sum of the transformed list elements
    """
    transformed_numbers = [user_function(num) for num in numbers]  # Apply function to each element
    return sum(transformed_numbers)  # Return the sum of the transformed elements
# Example user-defined function (e.g., squaring the number)
def square(x):
    return x ** 2

numbers = [1, 2, 3, 4, 5]
result = apply_and_sum(numbers, square)
print(result)

# lesson 8

# Task 1
def before_and_after_decorator(func):
    """
    A decorator that performs an action before and after the execution
    of the wrapped function.

    :param func: Function to be decorated
    :return: Wrapper function with added behavior
    """

    def wrapper(*args, **kwargs):
        print("Action before the function execution")  # Action before
        result = func(*args, **kwargs)  # Execute the original function
        print("Action after the function execution")  # Action after
        return result

    return wrapper
@before_and_after_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Alice")

# Task 2

import pickle
import os


def cache_to_file(filename):
    """
    A decorator that caches the results of the function to a file
    using pickle for serialization.

    :param filename: The name of the file where the cache will be stored
    :return: Decorated function with caching functionality
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = (args, frozenset(kwargs.items()))  # Create a unique key for the function call
            cache_file = f"{filename}.pkl"

            # Load the cache from the file if it exists
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    cache = pickle.load(f)
            else:
                cache = {}

            # Check if the result is in the cache
            if cache_key in cache:
                print("Returning cached result")
                return cache[cache_key]

            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache[cache_key] = result

            # Save the cache to the file
            with open(cache_file, 'wb') as f:
                pickle.dump(cache, f)

            return result

        return wrapper

    return decorator
@cache_to_file('cached_results')
def expensive_function(x, y):
    print(f"Calculating result for ({x}, {y})")
    return x ** y

# Call the function
print(expensive_function(2, 3))  # This will calculate and cache the result
print(expensive_function(2, 3))  # This will return the cached result
print(expensive_function(3, 2))  # This will calculate and cache the result for a new input

# Task 3

def handle_exceptions(func):
    """
    A decorator that intercepts and handles exceptions raised by the function.

    :param func: The function to decorate
    :return: A wrapper function that catches and handles exceptions
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Here you can handle different types of exceptions differently if needed
            # For example, you might want to log the error, re-raise it, etc.
            # raise  # Uncomment to re-raise the exception after handling it

    return wrapper


# Example usage
@handle_exceptions
def divide(a, b):
    """
    Divides two numbers and raises an exception for division by zero.

    :param a: The numerator
    :param b: The denominator
    :return: The result of the division
    """
    return a / b


# Testing the function
divide(5, 0)  # This will trigger an exception, which will be handled by the decorator

# Task 4

import time


def measure_time(func):
    """
    A decorator that measures and prints the execution time of the function.

    :param func: The function to decorate
    :return: A wrapper function that measures the execution time
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time  # Calculate the execution time
        print(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")
        return result  # Return the result of the function

    return wrapper


# Example usage
@measure_time
def some_function():
    """
    A function that sleeps for 2 seconds to simulate a time-consuming task.
    """
    time.sleep(2)


# Testing the function
some_function()  # This will print the execution time of the function

# Task 5

def log_arguments_results(func):
    """
    A decorator that logs the arguments and the result of the function.

    :param func: The function to decorate
    :return: A wrapper function that logs arguments and result
    """

    def wrapper(*args, **kwargs):
        # Log the arguments and keyword arguments
        print(f"Arguments for {func.__name__}: args={args}, kwargs={kwargs}")

        # Call the actual function and get the result
        result = func(*args, **kwargs)

        # Log the result
        print(f"Result of {func.__name__}: {result}")

        return result  # Return the result of the function

    return wrapper


# Example usage
@log_arguments_results
def add_numbers(a, b):
    """
    Adds two numbers and returns the result.

    :param a: First number
    :param b: Second number
    :return: Sum of a and b
    """
    return a + b


# Testing the function
add_numbers(3, 4)

# Task 6

def limit_calls(max_calls):
    """
    Decorator to limit the number of times a function can be called.

    :param max_calls: Maximum number of allowed calls
    :return: A decorator function
    """

    def decorator(func):
        # Variable to keep track of the number of calls
        call_count = 0

        def wrapper(*args, **kwargs):
            nonlocal call_count  # Use the call_count from the outer scope
            if call_count >= max_calls:
                print(f"Function {func.__name__} has reached the call limit of {max_calls}.")
                return  # Return without calling the actual function
            call_count += 1
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Example usage
@limit_calls(3)
def some_function():
    print("Function called")


# Testing the function
some_function()  # Output: Function called
some_function()  # Output: Function called
some_function()  # Output: Function called
some_function()  # Output: Function some_function has reached the call limit of 3.

# Task 7

def cache_results(func):
    """
    Decorator to cache the results of a function based on its arguments.

    :param func: Function to cache results for
    :return: Wrapper function with caching
    """
    cache = {}

    def wrapper(*args):
        if args in cache:
            # Return cached result if available
            return cache[args]
        result = func(*args)
        # Cache the result for future calls
        cache[args] = result
        return result

    return wrapper


@cache_results
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Testing the function
print(fibonacci(10))  # Calculated
print(fibonacci(10))  # Cached


