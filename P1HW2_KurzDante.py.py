# Dante Kurz
# 3/28/2026
# P1HW2 - Python Basics
# Program that calculates and displays travel expenses

# Get user input for travel expenses
print("This program calculates and displays your travel expenses.")
print()
budget = float(input("Enter  budget: "))
print()
destination = input("Enter your travel destination: ")
print()
gas_cost = float(input("How much do you think you will spend on gas: "))
print()
accommodation_cost = float(input("Approximately, how much will you spend on accommodation: "))
print()
food_cost = float(input("Last, how much do you need for food: "))
print()

# Calculate total expenses
print("--------------------Travel Expenses--------------------")
print(f"Destination: {destination}")
print(f"Initial Budget: ${budget:.2f}")
print()
print(f"Fuel: ${gas_cost:.2f}")
print(f"Accommodation: ${accommodation_cost:.2f}")
print(f"Food: ${food_cost:.2f}")
print()
# Calculate remaining budget
remaining_budget = budget - (gas_cost + accommodation_cost + food_cost)
print(f"Remaining budget: ${remaining_budget:.2f}")