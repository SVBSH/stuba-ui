import heapq
from lib.draw import plot_clusters
import numpy as np
from typing import Tuple

from lib.parse import process_command_line_arguments


def adjust_range(base_point_axis: int, space_range: Tuple[int, int], offset_range: Tuple[int, int]):
    min_offset = offset_range[0]
    max_offset = offset_range[1]

    min_diff = base_point_axis + offset_range[0]
    if min_diff < space_range[0]:
        min_offset = offset_range[0] + abs(abs(min_diff) - abs(space_range[0]))

    max_diff = base_point_axis + offset_range[1]
    if max_diff > space_range[1]:
        max_offset = offset_range[1] - abs(abs(max_diff) - abs(space_range[1]))

    return min_offset, max_offset

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
    """
    Calculate the Manhattan dstance between two points
    """
    return np.sum(np.abs(point1 - point2))

def calculate_centroid(cluster):
    """
    Calculate the centroid of a given cluster
    """
    return np.mean(cluster, axis=0)
    

def hierarchical_clustering(data, max_clusters, use_medoids=False):
    data = np.array(data)
    n_points = len(data)
    # keep track of clusters
    clusters = {cluster_index: [cluster_index] for cluster_index in range(n_points)} 

    def calculate_centroid(cluster_indices):
        """calculate the centroid of the cluster"""
        return np.mean(data[cluster_indices], axis=0)

    def calculate_medoid(cluster_indices):
        """calculate the medoid of the cluster"""
        cluster_data = data[cluster_indices]
        distance_matrix = np.sum(np.abs(cluster_data[:, np.newaxis] - cluster_data), axis=2)
        medoid_index = np.argmin(np.sum(distance_matrix, axis=1))
        return cluster_data[medoid_index]

    # choose the heuristic function
    calculate_cluster_center = calculate_medoid if use_medoids else calculate_centroid

    # preprocess all distances and store them in the dictionary
    distances = {}
    for i in range(n_points):
        for j in range(i+1, n_points):
            distance = manhattan_distance(data[i], data[j])
            distances[(i, j)] = distance

    # create a heap for distances
    distance_heap = [(dist, i, j) for (i, j), dist in distances.items()]
    heapq.heapify(distance_heap)

    while len(clusters) > max_clusters:
        # Find the closest pair of clusters
        while True:
            distance, i, j = heapq.heappop(distance_heap)
            if i in clusters and j in clusters and i != j:
                if distance == distances[(min(i, j), max(i, j))]:
                    break

        # Merge clusters and update distances
        new_cluster = clusters[i] + clusters[j]
        clusters[i] = new_cluster
        del clusters[j]

        # Update distances in the heap for the merged cluster using incremental updates
        new_center = calculate_cluster_center(new_cluster)
        for k in clusters:
            if k != i:
                other_center = calculate_cluster_center(clusters[k])
                new_distance = manhattan_distance(new_center, other_center)
                distances[(min(i, k), max(i, k))] = new_distance
                heapq.heappush(distance_heap, (new_distance, min(i, k), max(i, k)))

    # Prepare final clusters list
    return [data[index] for index in clusters.values()]


if __name__ == '__main__':

    # Example usage
    args = process_command_line_arguments()
    print("Additional Points:", args.additional_points)
    print("Use Medoids:", args.use_medoids)

    space_range = (-5000, 5000)
    initial_points = 20
    additional_points = args.additional_points
    offset_range = (-100, 100)

    # maximum number of clusters
    max_clusters = args.clusters

    coordinates = generate_random_points(initial_points, space_range, additional_points, offset_range)

    # Use the previously defined hac_with_max_clusters function
    hac_clusters = hierarchical_clustering(coordinates, max_clusters, use_medoids=args.use_medoids)

    # Plot the clusters
    plot_clusters(hac_clusters)
