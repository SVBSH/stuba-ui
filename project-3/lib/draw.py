import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from typing import Tuple


Coordinate: Tuple[int,int]


def draw(coordinates, min_val: int, max_val: int):
    # Separating the coordinates into x and y lists
    x_points, y_points = zip(*coordinates)

    fig, ax = plt.subplots()

    ax.set_title('20 Random Unique Points in 2D Space')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    
    # Plotting the points
    ax.plot(x_points, y_points, 'ro')
    plt.show()


def plot_clusters(coordinates, clusters):
    # Vytvorenie farieb pre zhluky
    colors = cm.rainbow(np.linspace(0, 1, len(clusters)))

    # Vytvorenie nového obrázka
    plt.figure()

    for cluster, color in zip(clusters, colors):
        # Vyberieme body v aktuálnom zhluku
        cluster_points = coordinates[cluster]

        # Vykreslenie bodov
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color)

    # Pridanie titulku a popisiek osí
    plt.title("Aglomeratívne zhlukovanie")
    plt.xlabel("X súradnica")
    plt.ylabel("Y súradnica")

    # Zobrazenie grafu
    plt.show()


def plot_clusters_1(clusters):
    """Plot the clusters with different colors and add a label for each cluster."""
    colors = cm.rainbow(np.linspace(0, 1, len(clusters)))
    for idx, (cluster, color) in enumerate(zip(clusters, colors)):
        cluster_points = np.array(cluster)
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color)

        # Compute the centroid of the cluster for labeling
        centroid = np.mean(cluster_points, axis=0)
        plt.text(centroid[0], centroid[1], f'Cluster {idx+1}', fontsize=12, ha='center', va='center')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Hierarchical Agglomerative Clustering with Cluster Labels')
    plt.show()
