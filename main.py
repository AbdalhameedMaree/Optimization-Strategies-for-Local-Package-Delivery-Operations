import sys
from SA import simulated_annealing
from GA import GeneticAlgorithm  # Assume you have this
from vehicle import Vehicle
from package import Package
from plot import plot_best_vehicle_routes
import matplotlib.pyplot as plt
import math

class DeliveryInterface:
    def __init__(self):
        self.vehicles = []
        self.packages = []
        self.algorithm = None
        self.params = {}

    def show_menu(self):
        while True:
            print("\n===== Delivery Optimization =====")
            print("1. Load Vehicle File")
            print("2. Load Package File")
            print("3. Set Algorithm Parameters")
            print("4. Run Optimization and show results")
            print("5. Exit")
            
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.load_vehicles()
            elif choice == '2':
                self.load_packages()
            elif choice == '3':
                self.set_parameters()
            elif choice == '4':
                self.run_optimization()
            elif choice == '5':
                sys.exit()
            else:
                print("Invalid choice!")

    def load_vehicles(self):
        try:
            V = Vehicle(0, 0)
            self.vehicles = V.load_vehicle_file()
            print(f"Loaded {len(self.vehicles)} vehicles")
        except Exception as e:
            print(f"Error loading vehicles: {str(e)}")

    def load_packages(self):
        try:
            P = Package((0, 0), 0, 0)
            self.packages = P.load_package_file()
            print(f"Loaded {len(self.packages)} packages")
        except Exception as e:
            print(f"Error loading packages: {str(e)}")

    def set_parameters(self):
        print("\n===== Algorithm Selection =====")
        print("1. Simulated Annealing")
        print("2. Genetic Algorithm")
        algo_choice = input("Select algorithm: ").strip()
    
        if algo_choice == '1':
            self.algorithm = 'SA'
            print("\nSimulated Annealing Parameters:")
            self.params['cooling_rate'] = float(input("Cooling rate (0.90-0.99): "))
            
        elif algo_choice == '2':
            self.algorithm = 'GA'
            print("\nGenetic Algorithm Parameters:")
            self.params['num_generations'] = int(input("Number of generations (e.g., 100): "))
            self.params['pop_size'] = int(input("Population size (50-100): "))
            self.params['mutation_rate'] = float(input("Mutation rate (0.01-0.1): "))

    def run_optimization(self):
        if not self.vehicles or not self.packages:
            print("Load vehicles and packages first!")
            return
            
        if self.algorithm == 'SA':
            print("\nRunning Simulated Annealing...")
            self.best_state , self.cost_with_penalty = simulated_annealing(
                self.vehicles, 
                self.packages,
                cooling_rate=self.params.get('cooling_rate', 0.95)
            )
            
        elif self.algorithm == 'GA':
            print("\nRunning Genetic Algorithm...")
            self.best_state , self.cost_with_penalty  = GeneticAlgorithm(
                self.vehicles,
                self.packages,
                self.params.get('num_generations', 100),  # Correct order
                self.params.get('pop_size', 50),
                self.params.get('mutation_rate', 0.05)
            )
            
        print("Optimization complete!")
        self.show_results()
        self.plot_routes()

    def show_results(self):
        if not hasattr(self, 'best_state'):
            print("Run optimization first!")
            return
            
        total_cost = 0
        for idx, vehicle in enumerate(self.best_state):
            vehicle.route.insert(0,(0,0))
            dist = sum(math.dist(vehicle.route[i], vehicle.route[i+1]) 
                      for i in range(len(vehicle.route)-1))
            total_cost += dist
            print(f"\nVehicle {idx+1}:")
            print(f"Capacity: {vehicle.size}/{vehicle.capacity} kg")
            print(f"Route: {vehicle.route}")
            print(f"Distance: {dist:.2f} km")

        print(f"\nTotal System Distance Priority Penalty: {self.cost_with_penalty:.2f} km") 
        print(f"Total System Distance: {total_cost:.2f} km")

    def plot_routes(self):
        plot_best_vehicle_routes(self.best_state)
        plt.show()

if __name__ == "__main__":
    interface = DeliveryInterface()
    interface.show_menu()
