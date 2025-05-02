import random
import copy
import math
from plot import plot_best_vehicle_routes
import matplotlib.pyplot as plt


def total_cost(vehicles):
    # Existing distance cost
    lambda_param=0.3
    distance_cost = 0
    for vehicle in vehicles:
        if not vehicle.route:
            continue
        distance_cost += math.dist((0, 0), vehicle.route[0])
        for i in range(len(vehicle.route) - 1):
            distance_cost += math.dist(vehicle.route[i], vehicle.route[i + 1])
    
    priority_penalty = 0
    for vehicle in vehicles:
        for idx, package in enumerate(vehicle.packages):
            priority_penalty += package.priority * (idx + 1)        
     

    total = distance_cost + lambda_param * priority_penalty 
    return total

def random_package_distribution(vehicles, packages):
    for package in packages:
        possible_vehicles = [v for v in vehicles if v.capacity >= v.size + package.weight]
        if possible_vehicles:
            vehicle = random.choice(possible_vehicles)
            vehicle.packages.append(package)
            vehicle.route.append(package.destination)
            vehicle.size += package.weight  
    max_pac=0
    max_vex=0
    for package in packages:
        if package.weight > max_pac:
            max_pac = package.weight
    for vehcile in vehicles:
        if vehcile.capacity > max_vex:
            max_vex = vehcile.capacity 
    if max_pac > max_vex:
        print(f"\bcant store package with weight {max_pac} in any vehicle\n")
        exit()

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    
def generate_next_state(vehicles):
    operations = ["inner_swap", "outer_swap", "move"]
    op = random.choice(operations)
    new_vehicles = copy.deepcopy(vehicles)

    # Vehicles with at least one package
    non_empty_vehicles = [v for v in new_vehicles if v.packages]

    if op == "outer_swap":
        if len(non_empty_vehicles) < 2:
            return new_vehicles  # Not enough vehicles to swap between
        v1, v2 = random.sample(non_empty_vehicles, 2)
        p1 = random.choice(v1.packages)
        p2 = random.choice(v2.packages)
        r1 = v1.route[v1.packages.index(p1)]
        r2 = v2.route[v2.packages.index(p2)]
        v1.packages.remove(p1)
        v1.size -= p1.weight
        v2.packages.remove(p2)
        v2.size -= p2.weight
        v1.packages.append(p2)
        v1.size += p2.weight
        v2.packages.append(p1)
        v2.size += p1.weight
        v1.route.remove(r1)
        v2.route.remove(r2)
        v1.route.append(r2)
        v2.route.append(r1)

    elif op == "inner_swap":
        if not non_empty_vehicles:
            return new_vehicles
        v1 = random.choice(non_empty_vehicles)
        if len(v1.packages) < 2:
            return new_vehicles  # Not enough packages to swap
        p1, p2 = random.sample(v1.packages, 2)
        i1 = v1.packages.index(p1)
        i2 = v1.packages.index(p2)
        swap(v1.packages, i1, i2)
        swap(v1.route, i1, i2)

    elif op == "move":
        if len(non_empty_vehicles) < 1 or len(new_vehicles) < 2:
            return new_vehicles
        v1 = random.choice(non_empty_vehicles)
        v2_candidates = [v for v in new_vehicles if v != v1]
        if not v2_candidates:
            return new_vehicles
        v2 = random.choice(v2_candidates)
        if not v1.packages:
            return new_vehicles
        p1 = random.choice(v1.packages)
        i1 = v1.packages.index(p1)
        if i1 + 1 >= len(v1.route):
            return new_vehicles  # Prevent out-of-range
        r1 = v1.route[i1]
        v1.packages.remove(p1)
        v1.size -= p1.weight
        v1.route.remove(r1)
        v2.packages.append(p1)
        v2.size += p1.weight
        v2.route.append(r1)

    return new_vehicles


        
def total_cost(vehicles):
    # Existing distance cost
    lambda_param=0.3
    distance_cost = 0
    for vehicle in vehicles:
        if not vehicle.route:
            continue
        distance_cost += math.dist((0, 0), vehicle.route[0])
        for i in range(len(vehicle.route) - 1):
            distance_cost += math.dist(vehicle.route[i], vehicle.route[i + 1])
    
    priority_penalty = 0
    for vehicle in vehicles:
        for idx, package in enumerate(vehicle.packages):
            priority_penalty += package.priority * (idx + 1)        
     

    total = distance_cost + lambda_param * priority_penalty 
    return total

def is_valid (vehicles):
    for vehicle in vehicles:
        if vehicle.size > vehicle.capacity:
            return False
    return True

def simulated_annealing(vehicles, packages,cooling_rate):
    temperature = 1000
    min_temp = 1
    iterations_per_temp = 100

    random_package_distribution(vehicles, packages)
    current = vehicles

    # Initialize interactive plot
    plt.ion()
    fig, ax = None, None
    fig, ax = plot_best_vehicle_routes(current, ax, fig)
    step_count = 0
    plot_interval = 5  # Update plot every 5 temperature steps

    while temperature > min_temp:
        for _ in range(iterations_per_temp):
            while True:
                next_state = generate_next_state(current)
                if is_valid(next_state):
                    break
            delta = total_cost(next_state) - total_cost(current)
            if delta < 0:
                current = next_state
            else:
                probability = math.exp(-delta / temperature)
                if random.random() < probability:
                    current = next_state

        temperature *= cooling_rate
        # Force immediate terminal output
        print(f"Temp: {temperature:.2f}, Cost: {total_cost(current)}", flush=True)  # <-- Add flush=True

        # Update plot at intervals
        if step_count % plot_interval == 0:
            fig, ax = plot_best_vehicle_routes(current, ax, fig)
        step_count += 1

    # Close interactive plot to unblock terminal
    plt.ioff()
    plt.close(fig)  # <-- Close the figure explicitly
    return current
