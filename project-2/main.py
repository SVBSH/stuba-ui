import random
import math
from typing import List
from lib.parse import GlobalConfig, get_config
from lib.custom_types import Cities, Coordinate
from lib.draw import draw_route, initialize_canvas, DrawConfig


# User config
CONFIG: GlobalConfig = get_config()


def euclidean_distance(city_1: Coordinate, city_2: Coordinate):
    """Compute the Euclidean distance between two Cities."""
    return math.sqrt((city_1[0] - city_2[0])**2 + (city_1[1] - city_2[1])**2)


def create_distance_matrix(cities: Cities):
    """Create a distance matrix for list of cities"""
    num_cities = len(cities)
    distance_matrix = [
        [
            0 if city_1_index == city_2_index 
                else euclidean_distance(cities[city_1_index], cities[city_2_index]) 
                for city_2_index in range(num_cities)
        ] 
        for city_1_index in range(num_cities)]
    return distance_matrix


def calculate_total_distance(matrix, solution):
    """Calculate the total distance of tour between cities"""
    total_distance = 0
    for i in range(len(solution)):
        total_distance += matrix[solution[i - 1]][solution[i]]

    return total_distance


def swap_2opt(route, i, k):
    """
    Swap the endpoints of two edges by reversing a section of nodes,
    typically between node i and node k.
    2-opt heuristic pseudo code: https://en.wikipedia.org/wiki/2-opt

    1. take route[0] to route[v1] and add them in order to new_route
    2. take route[v1+1] to route[v2] and add them in reverse order to new_route
    3. take route[v2+1] to route[start] and add them in order to new_route
    """
    new_route = route[0:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route
    

def tabu_search(
        distance_matrix, 
        initial_solution: Cities, 
        cities: Cities, 
        debug_mode: bool,
        draw_config: DrawConfig,
        iterations=100, 
        tabu_size=100):
    """
    Perform tabu search with 2-opt heuristic for finding neighborhood
    """
    best_solution = initial_solution[:]
    best_cost = calculate_total_distance(distance_matrix, best_solution)
    tabu_list: List[Coordinate] = []


    while iterations > 0 or len(tabu_list) > tabu_size:

        neighborhood = []
        for neighb_a_index in range(1, len(best_solution) - 1):
            for neighb_b_index in range(neighb_a_index + 1, len(best_solution)):
                if (neighb_a_index, neighb_b_index) not in tabu_list:
                    new_route = swap_2opt(best_solution, neighb_a_index, neighb_b_index)
                    new_cost = calculate_total_distance(distance_matrix, new_route)
                    # optimize
                    neighborhood.append((new_route, new_cost, neighb_a_index, neighb_b_index))

        neighborhood.sort(key=lambda x: x[1])
        for new_route, new_cost, neighb_a_index, neighb_b_index in neighborhood:
            if new_cost < best_cost:
                best_solution, best_cost = new_route, new_cost

                if debug_mode:
                    draw_route(draw_config, cities, best_solution)

            tabu_list.append((neighb_a_index, neighb_b_index))
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
            break

        iterations -= 1


    if debug_mode:
        draw_route(draw_config, cities, best_solution)
        draw_config['window'].mainloop()

    return best_solution, best_cost


def get_city_coordinates() -> Cities:
    if CONFIG['randomized_cities']:
        return [
            (random.randint(0, CONFIG['plan_width']), random.randint(0, CONFIG['plan_height'])) 
            for _ in range(CONFIG['city_count'])]

    return [
        (60, 200), (180, 200), (100, 180), (140, 180), (20, 160), 
        (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), 
        (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), 
        (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]


def get_initial_solution(cities: Cities) -> List[int]:
    return list(range(len(cities)))


def main():
    cities_coordinates = get_city_coordinates()
    distance_matrix = create_distance_matrix(cities_coordinates)
    initial_solution = get_initial_solution(cities_coordinates)
    draw_config = initialize_canvas()

    best_solution, best_cost = tabu_search(
        distance_matrix,
        initial_solution,
        cities_coordinates,
        CONFIG['debug'],
        draw_config
    )

    print("Best solution:", best_solution)
    print("Best cost:", best_cost)


if __name__ == "__main__":
    main()
