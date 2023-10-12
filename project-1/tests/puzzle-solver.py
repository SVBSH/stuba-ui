from queue import PriorityQueue
from typing import List, Set, Dict, Callable, Optional
from math import sqrt
import argparse

from itertools import permutations
from time import time


GamePlan = List[int]
goal_state: GamePlan = [1, 2, 3, 4, 5, 6, 7, 8, 0]
initial_state: GamePlan = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def get_side_length(game_plan: GamePlan) -> int:
    game_plan_length = len(game_plan)
    return int(sqrt(game_plan_length))


def get_goal_state(game_plan_length: int) -> GamePlan:
    return [number for number in range(1, game_plan_length)] + [0]


def heuristic_misplaced_positions(game_plan: GamePlan) -> int:
    """
        Counts the number of tiles that are not in their correct 
        positions in the current state compared to the goal state. 
        Returns: count of misplaced tiles in the game plan
    """
    result = 0
    for index, number in enumerate(game_plan, start=1):
        if (number != 0 and number != index):
            result += 1
    return result


def heuristic_manhattan_distance(game_plan: GamePlan) -> int:
    """
        Returns: cum of Manhattan Distances between goal state and 
        current state of the game plan.
        Manhattan distance formula := |x1 - x2| + |y1 - y2|
        https://en.wikipedia.org/wiki/Taxicab_geometry
    """
    game_plan_side_length: int = get_side_length(game_plan)
    distance_sum = 0
    for index, value in enumerate(game_plan):
        if value == 0:
            continue
        # get position axis of a current value 
        current_position = (
            index // game_plan_side_length, 
            index % game_plan_side_length)
        # get goal position axis of the current value 
        goal_position = (
            (value - 1) // game_plan_side_length,
            (value - 1) % game_plan_side_length)
        # calculate a distance between current and goal positions
        axis_x_difference = current_position[0] - goal_position[0]
        axis_y_difference = current_position[1] - goal_position[1]
        distance = abs(axis_x_difference) + abs(axis_y_difference)
        distance_sum += distance

    return distance_sum


def is_solvable(game_plan: GamePlan) -> int:
    """
        verify if game is solvable
    """
    inversions = 0
    game_plan_length = len(game_plan)
    # get total number of inversions
    for compare_index in range(game_plan_length):
        for index in range(compare_index + 1, game_plan_length):
            if game_plan[compare_index] > game_plan[index] and game_plan[compare_index] != 0 and game_plan[index] != 0:
                inversions += 1
    return inversions % 2 == 0


def test_is_not_solvable():
    permutations_list = list(permutations(range(9)))
    # Filter out the permutations that are not solvable
    not_solvable = [p for p in permutations_list if not is_solvable(p)]
    # Convert the not solvable permutations to a list
    not_solvable_list = [list(p) for p in not_solvable]

    for combination in not_solvable_list:
        assert(solve_puzzle(combination, heuristic_manhattan_distance) is None)
        assert(solve_puzzle(combination, heuristic_misplaced_positions) is None)
    print('Tests passed')


def test_is_solvable():
    permutations_list = list(permutations(range(9)))
    # Filter out the permutations that are not solvable
    solvable_states = [p for p in permutations_list if is_solvable(p)]
    # Convert the not solvable permutations to a list
    solvable_states_list = [list(p) for p in solvable_states]

    for combination in solvable_states_list:
        assert(solve_puzzle(combination, heuristic_manhattan_distance) is not None)
        assert(solve_puzzle(combination, heuristic_misplaced_positions) is not None)
    print('Tests passed')



def get_neighbors_of_blank_tile(game_plan_side_length: int, empty_tile_index: int) -> List[int]:
    neighbors: List[int] = []
    move_left: bool = empty_tile_index % game_plan_side_length > 0
    move_right: bool = empty_tile_index % game_plan_side_length < game_plan_side_length - 1
    move_up: bool = empty_tile_index // game_plan_side_length > 0
    move_down: bool = empty_tile_index // game_plan_side_length < game_plan_side_length - 1
    if move_left:
        neighbors.append(empty_tile_index - 1)
    if move_right:
        neighbors.append(empty_tile_index + 1)
    if move_up:
        neighbors.append(empty_tile_index - game_plan_side_length)
    if move_down:
        neighbors.append(empty_tile_index + game_plan_side_length)
    return neighbors


def solve_puzzle(initial_state: GamePlan, heuristic: Callable[[GamePlan], int]) -> Optional[List[GamePlan]]:
    """
        solve 8 puzzle problem
    """
    game_plan_length = len(initial_state)
    game_plan_side_length = int(sqrt(game_plan_length))
    if not is_solvable(initial_state):
        return None
    
    if len(initial_state) == 0:
        print('Error: Invalid Game Plan')
        return None
    
    goal_state: GamePlan = get_goal_state(game_plan_length)
    visited: Set[str] = set()
    queue = PriorityQueue()
    # store steps and their parent states
    steps: Dict[str, GamePlan] = {}  

    # initialize queue
    queue.put((initial_state, heuristic(initial_state), 0))
    # initial state has no parent 
    steps[str(initial_state)] = None  
    index = 0
    while not queue.empty():
        current_state, _, step = queue.get()
        
        game_solved: bool = current_state == goal_state
        if game_solved:
            # reconstruct steps of the solution
            solution: List[GamePlan] = [current_state]

            while steps[str(current_state)] is not None:
                current_state = steps[str(current_state)]
                solution.append(current_state)

            solution.reverse()
            return solution

        visited.add(str(current_state))
        empty_tile_index = current_state.index(0)

        # generate successor states by moving the empty tile
        neighbors = get_neighbors_of_blank_tile(game_plan_side_length, empty_tile_index)
   

        for neighbor_index in neighbors:
            new_state: GamePlan = current_state.copy()
            # swap positions
            new_state[empty_tile_index], new_state[neighbor_index] = \
                new_state[neighbor_index], new_state[empty_tile_index]

            new_state_key = str(new_state)
            if new_state_key not in visited:
                queue.put((new_state, heuristic(new_state), step + 1))
                steps[new_state_key] = current_state
    return None


def print_game_plan(game_plan: GamePlan):
    game_plan_length = len(game_plan)
    game_plan_side_length = int(sqrt(game_plan_length))
    for row_index, value in enumerate(game_plan, start=1):
        sep = '\n' if row_index % game_plan_side_length == 0 else ' '
        print(f'{value:3}', end=sep)


def print_solution_steps(steps: List[GamePlan]):
    for step_index, step in enumerate(steps):
        print(f'Step: {step_index}')
        print_game_plan(step)   
        print()


def parse_user_options():
    parser = argparse.ArgumentParser(description='Puzzle Solver - 8 puzzle problem solver')
    parser.add_argument('-s', '--initial-state', type=str, default="0,1,2,3,4,5,6,7,8", help='initial state of the puzzle')
    parser.add_argument('-t', '--heuristic', type=int, choices=[1, 2], default=1, help='\
                        Specify heuristic function OPTION. Default value is 1.\n\
                        OPTION 1: Manhattan distance heuristic\
                        OPTION 2: Heuristic of misplaced tiles in the game plan')
    parser.add_argument('-v', '--verbose', action='store_true', help=' \
            Enable verbose mode. If program found a solution then it print all the steps \
            from start state to the goal state. If the solution is not found it will \
            notice you with a message.')
    parser.add_argument('-e', '--run-tests', type=int, choices=[1, 2], default=1, help='Run tests')
    
    args = parser.parse_args()

    if args.run_tests:
        if args.run_tests == 1:
            test_is_not_solvable()
        elif args.run_tests == 2:
            test_is_solvable()
        return

    if args.initial_state:
        initial_state = [int(number) for number in args.initial_state.split(',')]
        if len(initial_state) == 0:
            print('Invalid initial state')
            return -1
    
    if args.heuristic == 1:
        heuristic_function = heuristic_manhattan_distance
    elif args.heuristic == 2:
        heuristic_function = heuristic_misplaced_positions

    if heuristic_function is not None:
        solution = solve_puzzle(initial_state, heuristic_function)
    
    if args.verbose:
        print('Solution was found!\nSteps:\n')
        if solution is not None:
            print_solution_steps(solution)
        else:
            print('The game is not solvable')


if __name__ == '__main__':
    parse_user_options()