class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.size = 0
        self.packages = []
        self.route = []

    def load_vehicle_file(self, filename="Vehicle.txt"):
        list_of_vehicles = []
        with open(filename, "rt") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue 
                try:
                    capacity = float(line)
                    v = Vehicle(i, capacity)
                    list_of_vehicles.append(v)
                except ValueError:
                    print(f"Invalid capacity value on line {i}: '{line}'")
                    exit()
        return list_of_vehicles

