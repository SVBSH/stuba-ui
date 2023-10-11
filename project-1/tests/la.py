from queue import PriorityQueue
from typing import List, Set, Dict, Callable, Optional
from math import sqrt
from itertools import permutations

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
    inversions = 0
    game_plan_length = len(game_plan)
    # get total number of inversions
    for i in range(game_plan_length):
        for j in range(i + 1, game_plan_length):
            if game_plan[i] > game_plan[j] and game_plan[i] != 0 and game_plan[j] != 0:
                inversions += 1
    return inversions % 2 == 0


def test_is_solvable():
    permutations_list = list(permutations(range(9)))
    # Filter out the permutations that are not solvable
    not_solvable = [p for p in permutations_list if is_solvable(p)]
    # Convert the not solvable permutations to a list
    not_solvable_list = [list(p) for p in not_solvable]
    index = 0
    for combination in not_solvable_list:
        index += 1
        if solve_puzzle(combination, heuristic_misplaced_positions) is None:
            # print(f'not solvable: {combination}')
            print('not solvable: ', combination)
            print(index)
            exit(1)
            pass
        else:
            print(index)
            # print(f'solvable: {combination}')
            # exit(1)
        continue
        game_plan_length = len(combination)
        game_plan_side_length = int(sqrt(game_plan_length))
        if is_solvable(combination, game_plan_side_length):
            # print(f'solvable: {combination}')
            pass
        else:
            print(f'not solvable: {combination}')
            exit(1)
        # if (index == 3):
        #     return


def get_neighbors_of_blank_tile(game_plan_side_length: int, empty_tile_index: int):
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

            if str(new_state) not in visited:
                queue.put((new_state, heuristic(new_state), step + 1))
                steps[str(new_state)] = current_state
    return None


def print_game_plan(game_plan: GamePlan):
    game_plan_length = len(game_plan)
    game_plan_side_length = int(sqrt(game_plan_length))
    for row_index, value in enumerate(game_plan, start=1):
        sep = '\n' if row_index % game_plan_side_length == 0 else ' '
        print(f'{value:3}', end=sep)            


test_is_solvable()

# Solve the puzzle
combination = [
1,2,3,4,5,
6,7,8,9,10,
11,12,13,0,14,
16,17,18,19,15,
21,22,23,24,20
]
# solve_puzzle(combination, heuristic_manhattan_distance)
# ss = is_solvable(combination, game_plan_side_length)
# print(ss)

# solution_steps = solve_puzzle(combination, heuristic_manhattan_distance)
# if solution_steps:
#     print("Solution found:")
#     for step, game_plan in enumerate(solution_steps, start=1):
#         print(f'-> Step: {step}')
#         print_game_plan(game_plan)
#         print()
# else:
#     print("No solution found.")


# print(solve_puzzle(combination, heuristic_misplaced_positions)
# )
# print(combination)
# print(get_inversion_count(combination))

# sis = is_solvable(combination, game_plan_side_length)
# print(sis)