import random
import math
import tkinter as tk
import time
from typing import List, Tuple
from parse import GlobalConfig, get_config


Coordinate = Tuple[int, int]
Cities = List[Coordinate]
CONFIG: GlobalConfig = get_config()


def euclidean_distance(city_1: Coordinate, city_2: Coordinate):
    """Compute the Euclidean distance between two points."""
    return math.sqrt((city_1[0] - city_2[0])**2 + (city_1[1] - city_2[1])**2)


def create_distance_matrix(cities: Cities):
    """Create a distance matrix for the given list of cities."""
    num_cities = len(cities)
    distance_matrix = [[0 if city_1_index == city_2_index else euclidean_distance(cities[city_1_index], cities[city_2_index]) 
                        for city_2_index in range(num_cities)] for city_1_index in range(num_cities)]
    return distance_matrix


def calculate_total_distance(matrix, solution):
    """Calculate the total distance of tour between cities"""
    total_distance = 0
    for i in range(len(solution)):
        total_distance += matrix[solution[i - 1]][solution[i]]

    return total_distance


def swap_2opt(route, i, k):
    """Swap the endpoints of two edges by reversing a section of nodes,
       typically between node i and node k."""
    # c <-> f
    # a b c d e f g
    # a | f e d c b | f g
    new_route = route[0:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route
    

def draw_route(canvas, cities: Cities, route):
    """Function to draw the tour in a Tkinter canvas."""
    # Clear the canvas
    canvas.delete("all")

    # Normalize the city coordinates
    max_width = max(city[0] for city in cities) + 10
    max_height = max(city[1] for city in cities) + 10
    scaled_cities = [(x / max_width * 480 + 10, y / max_height * 480 + 10) for x, y in cities]

    # Draw the cities
    for x, y in scaled_cities:
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')

    # Draw the route
    for i in range(-1, len(route) - 1):
        x1, y1 = scaled_cities[route[i]]
        x2, y2 = scaled_cities[route[i + 1]]
        canvas.create_line((x1, y1), (x2, y2), fill='blue', width=2)


def tabu_search(
        distance_matrix, 
        initial_solution, 
        window, 
        canvas, 
        cities, 
        debug_mode,
        iterations=100, 
        tabu_size=100, 
        max_tabu_size=100):
    """
    Perform tabu search with 2-opt heuristic for finding neighborhood
    2-opt heuristic: https://en.wikipedia.org/wiki/2-opt
    """
    best_solution = initial_solution[:]
    best_cost = calculate_total_distance(distance_matrix, best_solution)
    tabu_list = []


    while iterations > 0 or len(tabu_list) > max_tabu_size:

        neighborhood = []
        for neighb_a_index in range(1, len(best_solution) - 1):
            for neighb_b_index in range(neighb_a_index + 1, len(best_solution)):
                if (neighb_a_index, neighb_b_index) not in tabu_list:
                    new_route = swap_2opt(best_solution, neighb_a_index, neighb_b_index)
                    new_cost = calculate_total_distance(distance_matrix, new_route)
                    neighborhood.append((new_route, new_cost, neighb_a_index, neighb_b_index))

        new_best = False
        # so
        neighborhood.sort(key=lambda x: x[1])
        for new_route, new_cost, neighb_a_index, neighb_b_index in neighborhood:
            if (neighb_a_index, neighb_b_index) not in tabu_list or new_cost < best_cost:
                if new_cost < best_cost:
                    best_solution, best_cost = new_route, new_cost

                    if debug_mode:
                        draw_route(canvas, cities, best_solution)
                        window.update_idletasks()
                        window.update()
                        time.sleep(0.1)

                tabu_list.append((neighb_a_index, neighb_b_index))
                if len(tabu_list) > tabu_size:
                    tabu_list.pop(0)
                break
            
        iterations -= 1


    if debug_mode:
        draw_route(canvas, cities_coordinates, best_solution)
        window.mainloop()

    return best_solution, best_cost


def get_city_coordinates() -> Cities:
    if CONFIG['randomized_cities']:
        return [(random.randint(0, 500), random.randint(0, 500)) for _ in range(CONFIG['city_count'])]

    return [
        (60, 200), (180, 200), (100, 180), (140, 180), (20, 160), 
        (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), 
        (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), 
        (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]


def get_initial_solution(cities: Cities) -> List[int]:
    return list(range(len(cities)))


if __name__ == "__main__":
    cities_coordinates = get_city_coordinates()
    distance_matrix = create_distance_matrix(cities_coordinates)
    initial_solution = get_initial_solution(cities_coordinates)
    # Create the Tkinter window
    window = tk.Tk()
    window.title("Tabu Search Visualization")

    # Create a canvas
    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()

    # Perform Tabu Search with live drawing
    best_solution, best_cost = tabu_search(
        distance_matrix,
        initial_solution,
        window,
        canvas,
        cities_coordinates,
        CONFIG['debug']
    )

    print("Best solution:", best_solution)
    print("Best cost:", best_cost)
