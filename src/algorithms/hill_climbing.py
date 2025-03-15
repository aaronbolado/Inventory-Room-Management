import random
import pandas as pd
import matplotlib.pyplot as plt

# Hill climb optimization for the best order quantity
def hill_climb(initial_solution, setup_cost, holding_cost, demand, step_size, product_cost, discounts_included, maximum=None):
    # If user has no initial solution, generate a random value
    if initial_solution is None or initial_solution == 0:
        if demand <= 1:
            initial_solution = random.randint(1, 1000)
        else:
            initial_solution = random.randint(1, int(demand))

    # Get discount table
    discounts = read_discounts(file_path= "src\\algorithms\\Quantity-Discounts.xlsx")

    # Initialize variables for hill climb
    count = 0
    current_quantity = initial_solution
    current_cost = evaluate_solution(initial_solution, setup_cost, demand, holding_cost, product_cost, discounts, discounts_included)

    # FOR LIST FOR PLOTTING GRAPH
    order_quantities = [current_quantity]
    costs = [current_cost]

    while maximum is None or count < maximum:
        # Update best solution
        count += 1
        best_quantity = current_quantity
        best_cost = current_cost

        # Generate neighboring solutions
        for neighbor_quantity in generate_neighbors(current_quantity, step_size):
            # Skip invalid neighbors
            if neighbor_quantity <= 0:
                continue

            neighbor_cost = evaluate_solution(neighbor_quantity, setup_cost, demand, holding_cost, product_cost, discounts, discounts_included)

            # Update best solution if the neighbor's cost is better
            if neighbor_cost < best_cost:
                best_quantity = neighbor_quantity
                best_cost = neighbor_cost
        
        # If lowest point reached, return current solution
        if best_quantity == current_quantity and step_size == 1:
            return current_quantity, current_cost, order_quantities, costs, count
        # Reduce step size if no better neighbor found
        elif best_quantity == current_quantity and step_size > 1:
            step_size = 1

        # Update the current solution to the best neighbor found
        current_quantity = best_quantity
        current_cost = best_cost

        # STORE DATA FOR PLOTTING GRAPH
        order_quantities.append(current_quantity)
        costs.append(current_cost)

    return current_quantity, current_cost, order_quantities, costs, count

# Create adjacent neigbors of the current solution
def generate_neighbors(reorder_quantity, step_size):
    neighbors = [
        reorder_quantity + step_size,
        reorder_quantity - step_size
    ]
    return neighbors

# Objective function for evaluating the current solution
def evaluate_solution(reorder_quantity, setup_cost, demand, holding_cost, product_cost, discounts, discounts_included):
    if discounts_included:
        # Get discount from discounts list based on quantity
        discount = 1 - get_discount(reorder_quantity, discounts)
    else:
        discount = 1

    # Modified EOQ formula to include discounts
    EOQ = ((setup_cost * demand) / reorder_quantity) + ((holding_cost * reorder_quantity) / 2) + ((product_cost * discount) * demand)
    print(f"Reorder Quantity: {reorder_quantity}, Cost: {EOQ}")
    return EOQ

def read_discounts(file_path):
    return pd.read_excel(file_path)

def get_discount(reorder_quantity, discounts):
    for index, row in discounts.iterrows():
        if row['Min Quantity'] <= reorder_quantity <= row['Max Quantity']:
            return row['Discount']
    return 0

# Plot the points
def plot_points(reorder_quantity, costs):
    plt.figure(figsize=(10, 6))
    plt.plot(reorder_quantity, costs, marker='o', linestyle='-')
    plt.xlabel('Reorder Quantity (Q)')
    plt.ylabel('Cost')
    plt.title('Hill Climbing Optimization')
    plt.grid(True)
    plt.show()