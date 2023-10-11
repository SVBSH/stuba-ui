from queue import PriorityQueue
from typing import List, Set, Dict, Callable, Optional
from math import sqrt
import yaml


GamePlan = List[int]

goal_state: GamePlan = [1, 2, 3, 4, 5, 6, 7, 8, 0]
initial_state: GamePlan = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def get_goal_state(game_plan_length: int) -> GamePlan:
    return [number for number in range(1, game_plan_length)] + [0]


def heuristic_misplaced_positions(game_plan: GamePlan) -> int:
    result = 0
    for index, number in enumerate(game_plan, start=1):
        if (number == 0):
            continue
        if (number != index):
            result += 1
    return result


# Define a function to calculate the misplaced tiles heuristic
def misplaced_tiles_heuristic(game_plan: GamePlan) -> int:
    return sum([1 for i, j in zip(game_plan, goal_state) if i != j])



def get_inversion_count(game_plan: GamePlan) -> int:
    """
        Calculates a count of inversions in the game plan
    """
    inversion_count = 0
    for comp_index, comp_value in enumerate(game_plan):
        if comp_value == 0:
            continue
        for index in range(comp_index, len(game_plan)):
            if game_plan[index] != 0 and comp_value > game_plan[index]:
                inversion_count += 1
    return inversion_count


def get_zero_position_row(game_plan: GamePlan, game_plan_side_length: int) -> int:
    for index, number in enumerate(game_plan, start=0):
        if number == 0:
            return index // game_plan_side_length
    return -1


def is_solvable(game_plan: GamePlan, game_plan_side_length: int) -> bool:
    inversion_count_end_state = 0 
    zero_position_row = get_zero_position_row(game_plan, game_plan_side_length)
    actual_inversion_count = get_inversion_count(game_plan)
    return (inversion_count_end_state % 2) == (actual_inversion_count % 2) and (zero_position_row == (2 % 2))


def test_is_solvable():
    with open('solvable.yaml', 'r') as file:
        parsed_file = yaml.safe_load(file)
        index = 0
        for combination in parsed_file:
            index += 1
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


# Implement BFS with heuristic and step tracking
def solve_puzzle(initial_state: GamePlan, heuristic: Callable[[GamePlan], int]) -> Optional[List[GamePlan]]:
    game_plan_length = len(initial_state)
    game_plan_side_length = int(sqrt(game_plan_length))
    if not is_solvable(initial_state, game_plan_side_length):
        return None
    
    if len(initial_state) == 0:
        print('Error: Invalid Game Plan')
        return None
    
    goal_state: GamePlan = get_goal_state(game_plan_length)
    visited: Set[str] = set()
    queue = PriorityQueue()
    steps: Dict[str, GamePlan] = {}  # Dictionary to store steps and their parent states

    # Enqueue the initial state with its heuristic value and step 0
    queue.put((initial_state, heuristic(initial_state), 0))
    steps[str(initial_state)] = None  # Initial state has no parent
    index = 0
    while not queue.empty():
        current_state, _, step = queue.get()
        

        if current_state == goal_state:
            # Solution found, backtrack steps
            solution: List[GamePlan] = [current_state]
            while steps[str(current_state)] is not None:
                current_state = steps[str(current_state)]
                solution.append(current_state)
            solution.reverse()
            return solution

        visited.add(str(current_state))

        # Generate successor states by moving the empty tile
        empty_position_index = current_state.index(0)
        neighbors = []
        if empty_position_index % game_plan_side_length > 0:
            neighbors.append(empty_position_index - 1)  # Move left
        if empty_position_index % game_plan_side_length < game_plan_side_length - 1:
            neighbors.append(empty_position_index + 1)  # Move right
        if empty_position_index // game_plan_side_length > 0:
            neighbors.append(empty_position_index - game_plan_side_length)  # Move up
        if empty_position_index // game_plan_side_length < game_plan_side_length - 1:
            neighbors.append(empty_position_index + game_plan_side_length)  # Move down
   

        for neighbor_index in neighbors:
            new_state: GamePlan = current_state.copy()
            # move
            new_state[empty_position_index], new_state[neighbor_index] = new_state[neighbor_index], new_state[empty_position_index]

            if str(new_state) not in visited:
                queue.put((new_state, heuristic(new_state), step + 1))
                # pp.pprint(queue.queue)
                # print()
                # if step == 3:
                    # return
                steps[str(new_state)] = current_state

    return None  # No solution found


def print_game_plan(game_plan: GamePlan):
    game_plan_length = len(initial_state)
    game_plan_side_length = int(sqrt(game_plan_length))
    for row_index, value in enumerate(game_plan, start=1):
        sep = '\n' if row_index % game_plan_side_length == 0 else ' '
        print(f'{value:3}', end=sep)            


# test_is_solvable()
# Solve the puzzle
# combination = [
# 1,2,3,4,5,
# 6,7,8,9,10,
# 11,12,13,0,14,
# 16,17,18,19,15,
# 21,22,23,24,20
# ]
# solution_steps = solve_puzzle(combination, heuristic_misplaced_positions)
# game_plan_length = len(combination)
# game_plan_side_length = int(sqrt(game_plan_length))

solution_steps = solve_puzzle(initial_state, heuristic_misplaced_positions)
if solution_steps:
    print("Solution found:")
    for step, game_plan in enumerate(solution_steps, start=1):
        print(f'-> Step: {step}')
        print_game_plan(game_plan)
        print()
else:
    print("No solution found.")


# print(solve_puzzle(combination, heuristic_misplaced_positions)
# )
# print(combination)
# print(get_inversion_count(combination))

# sis = is_solvable(combination, game_plan_side_length)
# print(sis)