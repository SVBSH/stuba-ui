import random
import math
from typing import List
from lib.parse import GlobalConfig, get_config
from lib.custom_types import Cities, Coordinate
from lib.draw import draw_route, initialize_canvas, DrawConfig
import matplotlib.pyplot as plt


# User defined Global Configuration
CONFIG: GlobalConfig = get_config()
DEFAULT_CITIES: Cities = [
        (60, 200), (180, 200), (100, 180), (140, 180), (20, 160), 
        (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), 
        (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), 
        (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]


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

    iteration = 1
    while iteration < iterations or len(tabu_list) > tabu_size:

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
                    draw_route(draw_config, cities, best_solution, iteration, iterations)


            tabu_list.append((neighb_a_index, neighb_b_index))
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
            break

        iteration += 1


    if debug_mode:
        draw_route(draw_config, cities, best_solution, iteration, iterations)
        draw_config['window'].mainloop()

    return best_solution, best_cost


def simulated_annealing(
        distance_matrix, 
        initial_solution: List[int], 
        cities: Cities, 
        debug_mode: bool,
        draw_config: DrawConfig, 
        stopping_temperature=0.00000001, 
        alpha=0.995, 
        max_iterations=1000):
    
    current_solution = initial_solution
    current_cost = calculate_total_distance(distance_matrix, current_solution)
    best_solution = list(current_solution)
    best_cost = current_cost
    temperature = 1.0 

    for iteration in range(max_iterations):
        # cool the system down
        temperature *= alpha
        if temperature < stopping_temperature:
            break

        # pick two random indexes of cities
        rand_indexes = random.sample(range(1, len(current_solution)), 2)
        # sort indexes for 2-opt (first must be lower than second)
        i, k = sorted(rand_indexes)
        new_solution = swap_2opt(current_solution, i, k)
        new_cost = calculate_total_distance(distance_matrix, new_solution)

        cost_diff = new_cost - current_cost
        # always accept better solutions and worse solutions accept only with 
        # certain probability
        if cost_diff < 0 or math.exp(-cost_diff / temperature) > random.random():
            current_solution = new_solution
            current_cost = new_cost

            # update the best solution
            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost

                if debug_mode:
                    draw_route(draw_config, cities, best_solution, iteration, max_iterations)

    if debug_mode:
        draw_route(draw_config, cities, best_solution, max_iterations, max_iterations)
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


def run_algorithm():
    cities_coordinates = get_city_coordinates()
    distance_matrix = create_distance_matrix(cities_coordinates)
    initial_solution: List[int] = get_initial_solution(cities_coordinates)
    draw_config = initialize_canvas()
    if CONFIG['algorithm'] == 'ts':
        best_solution, best_cost = tabu_search(
            distance_matrix,
            initial_solution,
            cities_coordinates,
            CONFIG['debug'],
            draw_config,
            iterations=CONFIG['max_iterations']
        )
    elif CONFIG['algorithm'] == 'sa':
        best_solution, best_cost = simulated_annealing(
            distance_matrix, 
            initial_solution,
            cities_coordinates, 
            CONFIG['debug'],
            draw_config,
            max_iterations=CONFIG['max_iterations'])
        
    print("Best solution:", best_solution)
    print("Best cost:", best_cost)


"""  Algorithm analyzys functions  """
def test_runs_same_params(run_count: int):
    cities_coordinates =  DEFAULT_CITIES
    
    distance_matrix = create_distance_matrix(cities_coordinates)
    initial_solution: List[int] = get_initial_solution(cities_coordinates)
    tabu_search_cost = []
    sim_annealing_cost = []

    for _ in range(run_count):
        _, sa_cost = simulated_annealing(
            distance_matrix, 
            initial_solution,
            cities_coordinates, 
            False,
            None,
            max_iterations=1000)
        sim_annealing_cost.append(sa_cost)

        _, ts_cost = tabu_search(
                distance_matrix,
                initial_solution,
                cities_coordinates,
                False,
                None,
                iterations=1000
            )
        tabu_search_cost.append(ts_cost)

    generate_graph(tabu_search_cost, sim_annealing_cost)


def sensitivity_analysis_alpha():
    alpha_values = [0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99]

    cities_coordinates =  [
            (random.randint(0, 500), random.randint(0, 500)) 
            for _ in range(30)]
    
    distance_matrix = create_distance_matrix(cities_coordinates)
    initial_solution: List[int] = get_initial_solution(cities_coordinates)
    results = {}
    for alpha in alpha_values:
        _, best_cost = simulated_annealing(distance_matrix, initial_solution, alpha, False, None)
        results[alpha] = best_cost
    
    plt.figure(figsize=(10, 6))
    alphas = list(results.keys())
    best_costs = list(results.values())
    plt.plot(alphas, best_costs, marker='o')
    plt.xlabel('Alpha value')
    plt.ylabel('Best Solution Cost')
    plt.title('Sensitivity of Simulated Annealing by changing alpha value')
    plt.grid(True)
    plt.show()
    return results


def sensitivity_analysis_tabu_size():
    cities_coordinates =  DEFAULT_CITIES
    
    distance_matrix = create_distance_matrix(cities_coordinates)
    initial_solution: List[int] = get_initial_solution(cities_coordinates)
    tabu_size_values = [i for i in range(0, 100, 50)]

    results = {}
    for tabu_size in tabu_size_values:
        _, best_cost = tabu_search(distance_matrix, initial_solution, tabu_size, False, None)
        # Assuming that lower cost is better.
        results[tabu_size] = best_cost
    plt.figure(figsize=(10, 6))
    tabu_sizes = list(results.keys())
    best_costs = list(results.values())
    plt.plot(tabu_sizes, best_costs, marker='o')
    plt.xlabel('Tabu List Size')
    plt.ylabel('Best Solution Cost')
    plt.title('Sensitivity of Tabu Search to Tabu List Size')
    plt.grid(True)
    plt.show()
    return results


def generate_graph(tabu_search_cost, sim_annealing_cost):
    # Now plot the results
    plt.figure(figsize=(10, 5))
    plt.plot(tabu_search_cost, label='Tabu Search')
    plt.plot(sim_annealing_cost, label='Simulated Annealing')

    plt.title('Traveling Salesman Algorithm Costs')
    plt.xlabel('Iteration')
    plt.ylabel('Cost')

    # Add a legend to distinguish the lines
    plt.legend()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    run_algorithm()
