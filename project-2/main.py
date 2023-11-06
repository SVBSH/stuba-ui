
import argparse
from typing import List, Tuple, Dict
import numpy as np
from random import shuffle
from math import pow, sqrt
import tkinter as tk
import time
Coordinate = Tuple[int, int]
GamePlan = List[int]
game_plan_config = {
    'plan_width': 10,
    'plan_height': 10,
    'city_count': 0
}

start_position = (0, 2)
cities = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
# cities = [(c[0]*3, c[1]*3) for c in cities]

print(cities)
def get_initial_solution(cities: List[Coordinate]) -> List[int]:
    """
        returns: randomized tour
    """
    city_initial_order: List[int] = list(range(len(cities)))
    shuffle(city_initial_order)
    return city_initial_order


def get_city_distance(coordinate_a, coordinate_b):
    return sqrt((coordinate_a[0] - coordinate_b[0])**2 + (coordinate_a[1] - coordinate_b[1])**2)


def get_route_distance(cities: List[Coordinate], route_plan: List[int]) -> int:
    total_distance = 0

    for route_index in range(len(route_plan) - 1):
        total_distance += get_city_distance(cities[route_index], cities[route_index + 1])

    return total_distance


def generate_neighborhood(num_cities, current_route):
    neighbors = []
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            neighbor_tour = current_route.copy()
            neighbor_tour[i], neighbor_tour[j] = neighbor_tour[j], neighbor_tour[i]
            neighbors.append(neighbor_tour)
    return neighbors


def draw_route(canvas, cities, current_route):
    for i in range(len(current_route) - 1):
        fst_index = current_route[i]
        nxt_index = current_route[i+1]
        canvas.create_line(
            cities[fst_index][0],
            cities[fst_index][1], 
            cities[nxt_index][0], 
            cities[nxt_index][1], 
            fill="blue", width=2, tags="tour")

    canvas.create_line(
        cities[current_route[-1]][0], 
        cities[current_route[-1]][1], 
        cities[current_route[0]][0], 
        cities[current_route[0]][1], 
        fill="blue", width=2, tags="tour")
    canvas.update()


# def generate_2opt_neighbors(tour):
#     neighbors = []
#     num_cities = len(tour)

#     for i in range(num_cities - 1):
#         for j in range(i + 2, num_cities):
#             neighbor_tour = tour[:i] + list(reversed(tour[i:j])) + tour[j:]
#             neighbors.append(neighbor_tour)

#     return neighbors

def two_opt(tour, i, j):
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour


def generate_2opt_neighbors(current_tour):
    neighbors = []
    num_cities = len(current_tour)
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            neighbor_tour = two_opt(current_tour, i, j)
            neighbors.append(neighbor_tour)
    return neighbors


def tabu_search(city_coordinates, max_iteration_amount: int, canvas, max_tabu_size: int = 100):
    if max_iteration_amount < 1:
        return False
    
    current_route = get_initial_solution(city_coordinates)
    bestCandidate = current_route.copy()
    bestCandidateDistance: int = get_route_distance(city_coordinates, bestCandidate)
    tabu_list = [bestCandidate]
    print(bestCandidate)

    num_cities = len(city_coordinates)
    while max_iteration_amount:
        canvas.delete("tour")  # Clear the previous tour from the canvas

        best_neighbor_fitness = 10000000

        max_iteration_amount -= 1
        # neighbors = generate_neighborhood(num_cities, current_route)
        neighbors = generate_2opt_neighbors(current_route)
        bestCandidate = neighbors[0]
        for neighbor in neighbors:
            distance = get_route_distance(cities, neighbor)
            if neighbor not in tabu_list and distance < best_neighbor_fitness:
                bestCandidate = neighbor
                bestCandidateDistance = distance
        
        if best_neighbor_fitness == -1:
            break

        current_route = bestCandidate
        tabu_list.append(bestCandidate)

        if len(tabu_list) >= max_tabu_size:
            tabu_list.pop(0) 

        # Draw the current tour on the canvas
        draw_route(canvas, cities, current_route)

    
    return bestCandidate, bestCandidateDistance
    

def generate_cities(game_plan, game_plan_config):
    pass


def print_game_plan(game_plan: GamePlan, game_plan_config):
    game_plan_length = len(game_plan)
    game_plan_size: int = game_plan_config['city_count']

    for row_index, value in enumerate(game_plan, start=1):
        sep = '\n' if row_index % game_plan_config['plan_width'] == 0 else ' '
        print(f'{value:3}', end=sep)


def parse_user_options(game_plan_config):
    parser = argparse.ArgumentParser(
        prog="Travelling Salesman Problem Solver", 
        description='Program finds the shortest route between a set of points and locations that must be visited')
    parser.add_argument('-s', '--map-size', type=str, default="10,10",\
                        help='Define a width and height of map in following format: width,height')
    parser.add_argument('-c', '--city-count', type=int, default=20, choices=range(20, 41), help='Define amount of the cities in the game plan. If not specified it will be set to 20')
    # TODO: implement algorithms
    parser.add_argument('-a', '--algorithm', type=int, required=True, choices=[1, 2], help='\
                        Specify algorithm OPTION. Default value is 1.\n\
                        OPTION 1: Tabu Search\
                        OPTION 2: Simulated annealing')
    # TODO: implement verbose mode
    parser.add_argument('-v', '--verbose', action='store_true', help=' \
            Enable verbose mode. If program found a solution then it print all the steps \
            from start state to the goal state. If the solution is not found it will \
            notice you with a message.')
    # TODO: implement testing
    parser.add_argument('-e', '--run-tests', type=int, choices=[1, 2], help='Run tests. \
                        OPTION 1: test not solvable states. OPTION 2: test all solvable states with both heuristics')
    
    args = parser.parse_args()
    # Set map Width and Height
    if args.map_size:
        map_sizes: List[int] = args.map_size.split(',', 2)
        if len(map_sizes) != 2:
            print('Error: invalid game plan width/height')
            return False

        game_plan_config['plan_width'] = int(map_sizes[0])
        game_plan_config['plan_height'] = int(map_sizes[1])


    game_plan_config['city_count'] = args.city_count
    if game_plan_config['plan_width'] * game_plan_config['plan_height'] < args.city_count:
        print(f'Error: city count can not be higher than the game size')
        return False

    print(game_plan_config)
    return True


if __name__ == '__main__':
    root = tk.Tk()
    root.title("TSP with Tabu Search")

    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()
    for x, y in cities:
        scale = 4
        canvas.create_oval((x - scale), (y - scale), (x + scale), (y + scale), fill="red")
    
    best_candidate, best_candidate_distance = tabu_search(cities, 10_000, canvas)
    draw_route(canvas, cities, best_candidate)
    
    root.mainloop()