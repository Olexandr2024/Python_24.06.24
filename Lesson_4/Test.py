def is_point_in_circle(x, y, radius):
    # Calculate the square of the distance from the origin to the point (x, y)
    distance_squared = x**2 + y**2
    # Check if the squared distance is less than or equal to the squared radius
    return distance_squared <= radius**2

# Radius of the circle
radius = 4

# Input coordinates of the point from the user
x = float(input("Enter the x-coordinate of the point: "))
y = float(input("Enter the y-coordinate of the point: "))

# Check if the point is inside the circle and print the result
if is_point_in_circle(x, y, radius):
    print(f"The point ({x}, {y}) is inside the circle with radius {radius}.")
else:
    print(f"The point ({x}, {y}) is outside the circle with radius {radius}.")
