
import math
import random

# Euclidean distance between two points
def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Generate initial population of chromosomes
def generate_chromosomes(vehicles, packages, population_size):
    num_vehicles = len(vehicles)
    population = []

    while len(population) < population_size:
        chromosome = []
        vehicle_loads = [0] * num_vehicles

        for pkg in packages:
            vehicle_indices = list(range(num_vehicles))
            random.shuffle(vehicle_indices)

            for v_idx in vehicle_indices:
                if vehicle_loads[v_idx] + pkg.weight <= vehicles[v_idx].capacity:
                    vehicle_loads[v_idx] += pkg.weight
                    chromosome.append(v_idx)
                    break
            else:
                # No vehicle can carry this package
                chromosome = None
                break

        if chromosome is not None:
            population.append(chromosome)

    return population

# Fitness function (lower is better)
def fitness(chrom, vehicles, packages):
    lambda_param = 0.3
    loads = [0] * len(vehicles)
    for i, v in enumerate(chrom):
        loads[v] += packages[i].weight
    if any(loads[i] > vehicles[i].capacity for i in range(len(vehicles))):
        return float('inf')  # Invalid

    total_dist = 0
    for v_idx in range(len(vehicles)):
        route = [(0, 0)] + [
            packages[i].destination
            for i, assigned in enumerate(chrom)
            if assigned == v_idx
        ] + [(0, 0)]
        for a, b in zip(route, route[1:]):
            total_dist += euclidean(a, b)

    total_prio = sum(packages[i].priority for i in range(len(chrom)))

    return total_dist + total_prio * lambda_param 

# Single-point crossover
def crossover(parent1, parent2, crossover_point):
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Random mutation
def mutate(chromosome, mutation_rate, num_vehicles):
    if random.random() < mutation_rate:
        idx = random.randint(0, len(chromosome) - 1)
        chromosome[idx] = random.randint(0, num_vehicles - 1)
    return chromosome


def GeneticAlgorithm(vehicles, packages, num_generations, population_size, mutation_rate):
    population = generate_chromosomes(vehicles, packages, population_size)
    if not population:
        print("Failed to generate valid initial population.")
        return None

    best_chromosome = None
    cost = 0
    for generation in range(num_generations):
        scored_population = [(chrom, fitness(chrom, vehicles, packages)) for chrom in population]
        scored_population = [p for p in scored_population if p[1] != float('inf')]

        if not scored_population:
            print("All chromosomes became invalid in generation", generation)
            break

        scored_population.sort(key=lambda x: x[1])
        best_chromosome = scored_population[0][0]
        cost = scored_population[0][1]
        survivors = [chrom for chrom, fit in scored_population[:len(scored_population) // 2]]
        new_population = []
        while len(new_population) < population_size:
            parent1 = random.choice(survivors)
            parent2 = random.choice(survivors)
            crossover_point = random.randint(1, len(parent1) - 1)
            child1, child2 = crossover(parent1, parent2, crossover_point)
            child1 = mutate(child1, mutation_rate, len(vehicles))
            child2 = mutate(child2, mutation_rate, len(vehicles))
            new_population.extend([child1, child2])

        population = new_population[:population_size]
        
    # Update vehicle routes and packages based on the best chromosome
    if best_chromosome is not None:
        for vehicle in vehicles:
            vehicle.packages = []
            # vehicle.route = [(0, 0)]  # Start at depot

        for i, v_idx in enumerate(best_chromosome):
            if v_idx < len(vehicles):  # Ensure valid vehicle index
                vehicle = vehicles[v_idx]
                package = packages[i]
                vehicle.packages.append(package)
                vehicle.route.append(package.destination)

        # # Add return to depot
        # for vehicle in vehicles:
        #     vehicle.route.append((0, 0))

    return vehicles , cost  # Now returns the list of vehicles with updated routes
