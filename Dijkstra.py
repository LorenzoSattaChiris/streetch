import numpy as np
import random as random
import heapq as heapq
from matplotlib import pyplot as plt
import itertools  

class DijkstraGridWithEnd:
    def __init__(self, size=100, obstacle_ratio=0.1):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.obstacles = set()
        self.generate_obstacles(obstacle_ratio)
        self.start = self.generate_random_point()
        self.intermediary_targets = [self.generate_random_point() for _ in range(2)]  # Two intermediary targets
        self.end = self.generate_random_point()  # One end point

    def generate_obstacles(self, obstacle_ratio):
        obstacle_count = int(self.size * self.size * obstacle_ratio)
        while len(self.obstacles) < obstacle_count:
            obstacle = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if obstacle not in self.obstacles:
                self.obstacles.add(obstacle)

    def generate_random_point(self):
        point = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        while point in self.obstacles:
            point = (random.randint(0, self.size-1), random.randint(0, self.size-1))
        return point

    def neighbors(self, node):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),   # Vertical and horizontal
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
        ]
        result = []
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.size and 0 <= neighbor[1] < self.size and neighbor not in self.obstacles:
                result.append(neighbor)
        return result

    def dijkstra(self, start, target):
        pq = []
        heapq.heappush(pq, (0, start))
        distances = {start: 0}
        previous_nodes = {start: None}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == target:
                break

            for neighbor in self.neighbors(current_node):
                distance = current_distance + 1  # Uniform cost
                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return previous_nodes

    def path_as_list(self, previous_nodes, target):
        path = []
        step = target
        while step is not None:
            path.append(step)
            step = previous_nodes.get(step)
        path.reverse()
        return path

    def solve_tsp_with_end(self):
        # Calculate all pairs shortest paths
        points = [self.start] + self.intermediary_targets + [self.end]
        all_paths = {}
        for pair in itertools.permutations(points, 2):
            previous_nodes = self.dijkstra(pair[0], pair[1])
            all_paths[pair] = self.path_as_list(previous_nodes, pair[1])

        # Optimal route for visiting all points
        min_route = None
        min_distance = float('inf')
        for permutation in itertools.permutations(self.intermediary_targets):
            current_route = [self.start] + list(permutation) + [self.end]
            current_distance = 0
            for i in range(len(current_route) - 1):
                current_distance += len(all_paths[(current_route[i], current_route[i+1])]) - 1
            if current_distance < min_distance:
                min_distance = current_distance
                min_route = current_route

        # Build the final path from the optimal route
        final_path = []
        for i in range(len(min_route) - 1):
            final_path += all_paths[(min_route[i], min_route[i+1])][:-1]
        final_path.append(min_route[-1])

        return final_path

# Create an instance of the class with intermediary targets and end, execute the algorithm
dijkstra_grid_with_end = DijkstraGridWithEnd()
final_path_with_end = dijkstra_grid_with_end.solve_tsp_with_end()

def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Redisplay the image with all targets, end, and the optimal path
def create_image_with_intermediary_and_end(grid_obj, path):
    # Extract grid details
    grid_size = grid_obj.size
    start = grid_obj.start
    intermediary_targets = grid_obj.intermediary_targets
    end = grid_obj.end
    obstacles = grid_obj.obstacles
    
    # Create an empty grid for visualization
    image = np.zeros((grid_size, grid_size, 3))  # Use 3 channels for RGB

    # Mark the obstacles
    for obstacle in obstacles:
        image[obstacle] = [0.5, 0.5, 0.5]  # Gray for obstacles

    # Mark the path
    for (x, y) in path:
        image[x, y] = [1, 0, 0]  # Red for the path

    # Mark the start and end points
    image[start] = [0, 1, 0]  # Green for start
    image[end] = [1, 0, 1]  # Purple for end
    for target in intermediary_targets:
        image[target] = [0, 0, 1]  # Blue for intermediary targets

    # Plotting
    plt.figure(figsize=(10, 10))
    plt.imshow(image, interpolation='nearest')
    plt.title(f'Grid Path Visualization with two Intermediary and one End Target\nTotal steps: {len(path)-1}')
    plt.scatter(start[1], start[0], color='green', s=100, label='Start')
    plt.scatter(end[1], end[0], color='purple', s=100, label='End')
    for target in intermediary_targets:
        plt.scatter(target[1], target[0], color='blue', s=100, label='Intermediary Target')
    plt.legend()
    plt.grid(False)
    plt.axis('off')
    plt.show()

# Redisplay the image with all intermediary targets, end, and the optimal path
# create_image_with_intermediary_and_end(dijkstra_grid_with_end, final_path_with_end)

def analyze_pathfinding_dynamic(iterations):
    grid_size = 100
    steps_per_iteration = []
    distance_differences = []  # List of lists for each intermediary target and the end point

    for _ in range(iterations):
        grid = DijkstraGridWithEnd(grid_size, obstacle_ratio=0.1)
        final_path = grid.solve_tsp_with_end()
        steps_per_iteration.append(len(final_path) - 1)

        # Calculate Euclidean vs path length differences for each target
        points = [grid.start] + grid.intermediary_targets + [grid.end]
        distances_real = []
        distances_euclidean = []
        for i in range(len(points) - 1):
            actual_path = grid.dijkstra(points[i], points[i+1])
            actual_path_list = grid.path_as_list(actual_path, points[i+1])
            distances_real.append(len(actual_path_list) - 1)
            distances_euclidean.append(euclidean_distance(points[i], points[i+1]))

        distance_diff = [abs(real - euc) for real, euc in zip(distances_real, distances_euclidean)]
        distance_differences.append(distance_diff)
    
    # Convert distance differences to a numpy array for per-target analysis
    distance_differences = np.array(distance_differences)
    average_steps = np.mean(steps_per_iteration)

    # Plotting steps per iteration
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(steps_per_iteration, marker='o', linestyle='-', color='b')
    plt.axhline(y=average_steps, color='r', linestyle='--')
    plt.title(f"Steps per Iteration ({iterations} iterations) with Average")
    plt.xlabel("Iteration")
    plt.ylabel("Steps")
    plt.grid(True)

    # Plotting distance differences
    plt.subplot(1, 2, 2)
    for i in range(distance_differences.shape[1]):
        plt.plot(distance_differences[:, i], label=f'Target {i+1}')
    plt.title("Distance Differences per Target")
    plt.xlabel("Iteration")
    plt.ylabel("Difference in Distance (in steps)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return average_steps, distance_differences

# Example of running the function with a variable number of iterations
analyze_pathfinding_dynamic(1000)

