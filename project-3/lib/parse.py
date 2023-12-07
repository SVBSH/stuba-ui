import argparse


def process_command_line_arguments():
    parser = argparse.ArgumentParser(description=
                                     "Hierarchical Agglomerative Clustering. "
                                    "This program performs clustering on a given dataset using either "
                                    "centroids or medoids based on the provided arguments.")

    parser.add_argument("-a", "--additional_points", type=int, default=100, 
                        help="The number of additional points to generate. Must be a non-negative integer.")
    parser.add_argument("-t", "--use_medoids", action='store_true', 
                        help="Use medoids for clustering instead of centroids. Default is False.")
    parser.add_argument("-c", "--clusters", type=int, required=True,
                    help="The maximum number of clusters.")

    args = parser.parse_args()
    return args
