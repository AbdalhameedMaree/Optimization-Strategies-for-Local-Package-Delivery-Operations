from vehicle import Vehicle
from package import Package
from SA import simulated_annealing
from plot import plot_best_vehicle_routes
import random



def main():
    # Load vehicle data
    V = Vehicle(0, 0)
    vehicles = V.load_vehicle_file()

    # Load package data
    P = Package((0, 0), 0, 0)
    packages = P.load_package_file()

    # Run Simulated Annealing
    optimized_vehicles = simulated_annealing(vehicles)

    # Plot the result
    plot_best_vehicle_routes(optimized_vehicles)

if __name__ == "__main__":
    main()
