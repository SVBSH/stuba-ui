import tkinter as tk
from typing import TypedDict
import time
from lib.custom_types import Cities


class DrawConfig(TypedDict):
    window: tk.Tk
    canvas: tk.Canvas


def draw_route(draw_config: DrawConfig, cities: Cities, route, redraw_time=0.1):
    """Draw the tour between cities"""
    draw_config['canvas'].delete("all")

    # Normalize the city coordinates
    max_width = max(city[0] for city in cities) + 10
    max_height = max(city[1] for city in cities) + 10
    scaled_cities = [
        (coord_x / max_width * 480 + 10, coord_y / max_height * 480 + 10) 
        for coord_x, coord_y in cities]

    # Draw the cities
    for x, y in scaled_cities:
        draw_config['canvas'].create_oval(x - 5, y - 5, x + 5, y + 5, fill='#000300')

    # Draw the route
    for i in range(-1, len(route) - 1):
        prev_city = scaled_cities[route[i]]
        curr_city = scaled_cities[route[i + 1]]
        draw_config['canvas'].create_line(prev_city, curr_city, fill='#02A9EA', width=2)
    
    draw_config['window'].update()
    time.sleep(redraw_time)


def initialize_canvas() -> DrawConfig:
    draw_config: DrawConfig = {} # type: ignore
    draw_config['window'] = tk.Tk()
    draw_config['window'].title("Traveling Salesman Problem Visualization")

    draw_config['canvas'] = tk.Canvas(draw_config['window'], width=500, height=500, background='#D8D2E1')
    draw_config['canvas'].pack()
    return draw_config
