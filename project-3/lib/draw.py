import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt


def plot_clusters(clusters):
    """
    Show the result of hierarchical clustering using 
    matplotlib.
    Every cluster has a different color and its label.
    """

    # generate colors for cluster
    colors = cm.rainbow(np.linspace(0, 1, len(clusters)))
    for idx, (cluster, color) in enumerate(zip(clusters, colors)):
        cluster_points = np.array(cluster)
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], color=color)

        # add cluster label to its centroid position
        centroid = np.mean(cluster_points, axis=0)
        plt.text(centroid[0], centroid[1], f'Cluster {idx + 1}', fontsize=12, ha='center', va='center')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Hierarchical Agglomerative Clustering')
    plt.show()
