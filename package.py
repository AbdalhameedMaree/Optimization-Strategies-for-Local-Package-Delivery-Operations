class Package:
    def __init__(self, destination, weight, priority):
        self.destination = destination 
        self.weight = weight
        self.priority = priority

    
    def load_package_file(self, filename="Package.txt"):
        list_of_package = []
        with open(filename, "rt") as file:
            for i, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    parts = line.strip().split()
                    # Parse (x,y) from string like "(3,4)"
                    destination_str = parts[0].strip("()")
                    x, y = map(float, destination_str.split(','))
                    destination = (x, y)
                    weight = float(parts[1])
                    priority = int(parts[2])
                    P = Package(destination, weight, priority)
                    list_of_package.append(P)
                except (ValueError, IndexError):
                    print(f"Invalid line at {i}: '{line.strip()}'")
                    exit()
        return list_of_package
    


