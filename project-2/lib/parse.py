from argparse import ArgumentTypeError 
# argparse types
from argparse import Namespace, ArgumentParser
from typing import Tuple, TypedDict


class GlobalConfig(TypedDict):
    """
        Custom type for game plan configuration
        https://peps.python.org/pep-0589/
    """
    plan_width: int
    plan_height: int
    city_count: int
    debug: bool
    randomized_cities: bool
    max_iterations: int
    algorithm: str


def check_map_size(value: str) -> Tuple[int, int]:
    try:
        dimensions = value.split(",", 3)
        if len(dimensions) > 2:
            raise ValueError
        
        width, height = (int(dimension) for dimension in dimensions)
        if width <= 0 or height <= 0:
            raise ValueError
    except ValueError:
        raise ArgumentTypeError("Map size must be two positive integers separated by a comma.")
    return width, height


def check_city_count(value: str) -> int:
    min_cities = 20
    max_cities = 40
    try:
        city_count = int(value)
        if not min_cities <= city_count <= max_cities:
            raise ValueError
    except ValueError:
        raise ArgumentTypeError(f"City count must be an integer between {min_cities} and {max_cities}.")
    return city_count


def parse_arguments() -> Namespace:
    """
    Parse and validate program arguments

    Validation is done by using custom type functions:
    https://docs.python.org/3/library/argparse.html#type
    """
    parser = ArgumentParser(
        prog="Travelling Salesman Problem Solver",
        description="Program finds the shortest route between a set of cities"
    )
    
    parser.add_argument("-s", "--map-size", 
                        type=check_map_size, 
                        default="500,500",
                        help="Define map width and height (format: width,height). Default is 500,500.")
    
    parser.add_argument("-c", "--city-count", 
                        type=check_city_count, 
                        default='20',
                        help="Number of cities (20-40). Default is 20.")
    
    parser.add_argument("-d", "--debug", 
                        action='store_true',
                        help="Debug mode shows an evolution of finding route using tkinter.")
    
    parser.add_argument("-r", "--randomized-cities", 
                        action='store_true',
                        help="Generate a random city coordinates for the CITY_COUNT")
    
    parser.add_argument("-m", "--max-iterations",
                        type=int,
                        default=100,
                        help="The maximum amount of program iterations")

    # Add subparsers for supported algorithms
    subparsers = parser.add_subparsers(dest='algorithm', required=True, help='Choose an algorithm.')

    ### subparser for Tabu Search ###
    parser_tabu_search = subparsers.add_parser('ts', help='Use Tabu Search algorithm')
    parser_tabu_search.add_argument('--tabu-size', type=int, default=100, help='The maximum size of the Tabu List')

    ### subparser for Simulated Annealing ###
    parser_sim_annealing = subparsers.add_parser('sa', help='Use Simulated Annealing algorithm')
    parser_sim_annealing.add_argument('--cooling-factor', type=float, help='Cooling factor')

    return parser.parse_args()


def get_config():
    args = parse_arguments()

    config: GlobalConfig = {
        'plan_width': args.map_size[0],
        'plan_height': args.map_size[1],
        'city_count': args.city_count,
        'debug': args.debug,
        'randomized_cities': args.randomized_cities,
        'max_iterations': args.max_iterations,
        'algorithm': args.algorithm
    }
    if args.debug:
        print('Game plan configuration:', config)
    return config


if __name__ == "__main__":
    get_config()
