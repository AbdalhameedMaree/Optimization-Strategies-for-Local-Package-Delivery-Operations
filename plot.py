import matplotlib.pyplot as plt

def plot_best_vehicle_routes(vehicles):
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow']
    shop = (0, 0)

    vehicle_routes = []
    vehicle_indices = []
    all_x, all_y = [shop[0]], [shop[1]]

    for idx, vehicle in enumerate(vehicles):
        if not vehicle.packages:
            continue
        route = [shop] + [p.destination for p in vehicle.packages] + [shop]
        vehicle_routes.append(route)
        vehicle_indices.append(idx)

        for dest in route:
            all_x.append(dest[0])
            all_y.append(dest[1])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(min(all_x) - 2, max(all_x) + 2)
    ax.set_ylim(min(all_y) - 2, max(all_y) + 2)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title("Best Vehicle Delivery Routes")
    ax.grid(True)

    # Plot shop
    ax.plot(shop[0], shop[1], 'ro', markersize=10, label='Shop')
    ax.text(shop[0] + 0.5, shop[1] + 0.5, 'Shop', fontsize=9)

    # Plot routes
    for idx, route in enumerate(vehicle_routes):
        x = [p[0] for p in route]
        y = [p[1] for p in route]
        ax.plot(x, y, color=colors[vehicle_indices[idx] % len(colors)], marker='o', markersize=6, label=f'Truck {vehicle_indices[idx]+1}')
        for point in route[1:-1]:
            ax.text(point[0]+0.2, point[1]+0.2, f'({point[0]:.1f},{point[1]:.1f})', fontsize=7)

    ax.legend(loc='upper left')
    plt.show()