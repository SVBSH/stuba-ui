import heapq
from lib.draw import plot_clusters_1
import numpy as np
from typing import Tuple



def adjust_range(value, space_range, offset_range):
    """Adjust the range for offset to ensure the new point is within the space range."""
    low, high = offset_range
    if value + low < space_range[0]:
        low = space_range[0] - value
    if value + high > space_range[1]:
        high = space_range[1] - value
    return low, high

def generate_random_points(num_points: int, 
                           space_range: Tuple[int, int], 
                           additional_points: int, 
                           offset_range: Tuple[int, int]):
    points = []
    # generate initial points
    while len(points) < num_points:
        x = np.random.randint(space_range[0], space_range[1])
        y = np.random.randint(space_range[0], space_range[1])

        if ((x, y) in points):
            continue

        points.append((x, y))

    count = 0
    while count != additional_points:
        base_point = points[np.random.randint(0, len(points))]

        offset_x = np.random.randint(*adjust_range(base_point[0], space_range, offset_range))
        offset_y = np.random.randint(*adjust_range(base_point[1], space_range, offset_range))

        new_point = base_point[0] + offset_x, base_point[1] + offset_y
        if new_point in points:
            continue

        count += 1
        points.append(new_point)
    
    return np.array(points)

def manhattan_distance(point1, point2):
    """Calculate the Manhattan distance between two points using NumPy for efficiency."""
    return np.sum(np.abs(point1 - point2))

def calculate_centroid(cluster):
    """Calculate the centroid of a given cluster using NumPy for efficiency."""
    return np.mean(cluster, axis=0)

def hac_optimized_with_heap(data, max_clusters):
    """Optimized Hierarchical Agglomerative Clustering using a min heap for efficient distance retrieval."""
    # Convert data to a NumPy array for efficient processing
    data = np.array(data)
    n_points = len(data)
    clusters = {i: [i] for i in range(n_points)}  # Dictionary to keep track of clusters

    # Function to calculate the centroid of a cluster
    def calculate_centroid(cluster_indices):
        return np.mean(data[cluster_indices], axis=0)

    # Create a min heap for distances
    distance_heap = []
    for i in range(n_points):
        for j in range(i+1, n_points):
            distance = manhattan_distance(data[i], data[j])
            heapq.heappush(distance_heap, (distance, i, j))

    while len(clusters) > max_clusters:
        # Find the closest pair of clusters
        while True:
            distance, i, j = heapq.heappop(distance_heap)
            if i in clusters and j in clusters and i != j:
                break

        # Merge clusters
        clusters[i].extend(clusters[j])
        del clusters[j]

        # Update distances in the heap for the merged cluster
        for k in clusters:
            if k != i:
                new_distance = manhattan_distance(calculate_centroid(clusters[i]), calculate_centroid(clusters[k]))
                heapq.heappush(distance_heap, (new_distance, i, k))

    # Prepare final clusters list
    final_clusters = [data[indices] for indices in clusters.values()]
    return final_clusters

# Example data (feel free to replace with your data)
data = [[2, 6], [3, 4], [3, 8], [4, 7], [6, 2], [7, 4], [8, 5], [9, 7]]
space_range = (-5000, 5000)
initial_points = 20
additional_points = 5000
offset_range = (-100, 100)
coordinates = generate_random_points(initial_points, space_range, additional_points, offset_range)

# Perform HAC with a maximum number of clusters
max_clusters = 18  # For example, let's stop clustering when there are 3 clusters

# Use the previously defined hac_with_max_clusters function
hac_clusters = hac_optimized_with_heap(coordinates, max_clusters)

# Plot the clusters
plot_clusters_1(hac_clusters)
