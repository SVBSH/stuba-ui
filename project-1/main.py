from typing import List
import hashlib
from queue import Queue


import pprint
pp = pprint.PrettyPrinter(width=41, compact=True)
visited_states = {}

start_state = [
    1, 0, 2, 
    3, 4, 5, 
    6, 7, 8
]


start_state = [1, 2, 3, 0, 4, 6, 7, 5, 8]
start_state = [1, 2, 3, 0, 4, 6, 7, 5, 8]
actual_state = []
end_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

GE = False
# l = (0, 1)


def get_position(x: int, y: int, state):
    # TODO: verify range for 'x' and 'y'
    x = x * 3
    return state[x+y]


def set_position(x:int, y:int, value: int, state):
    x = x * 3
    state['state'][x+y] = value
    return


def swap_position(pos_1, pos_2, state):
    temp = get_position(pos_1[0], pos_1[1], state['state'])
    set_position(
        pos_1[0], pos_1[1], get_position(pos_2[0], pos_2[1], state['state']), state 
    )
    set_position(pos_2[0], pos_2[1], temp, state)


def heuristic_1(state: List[str]) -> int:
    result = 0
    for index, number in enumerate(state, start=1):
        if (number == 0):
            continue
        if (number != index):
            result += 1
    return result


def print_game_plan(game_plan):
    for row_index, value in enumerate(game_plan, start=1):
        sep = '\n' if row_index % 3 == 0 else ' '
        print(value, end=sep)            


def get_possible_moves(zero_position):
    """
        1 2 3
        4 0 5
        6 7 8
    """
    results = []
    move_down = zero_position[0] + 1
    move_up = zero_position[0] - 1
    move_right = zero_position[1] + 1
    move_left = zero_position[1] -1
    if (0 <= move_down < 3):
        results.append((move_down, zero_position[1]))
    if (0 <= move_up < 3):
        results.append((move_up, zero_position[1]))
    if (0 <= move_left < 3):
        results.append((zero_position[0], move_left))
    if (0 <= move_right < 3):
        results.append((zero_position[0], move_right))
    return results


def solve_game(game_plan, zero_position):
    print(zero_position)

    if is_solvable(game_plan, zero_position_row):
        _solve_game(game_plan, zero_position)
    else:
        print('Game is not solvable')


def _solve_game(game_plan, zero_position):

    possible_moves = get_possible_moves(zero_position)
    print(f'possMoves: {possible_moves}')
    print('Before:')  
    print_game_plan(game_plan)
    # [position in possible moves, value]

    # get next move
    min_value = 1000
    next_steps = []
    for move in possible_moves:
        swap_position(zero_position, move, game_plan)
        curr_heuristic = heuristic_1(game_plan)
        if curr_heuristic < min_value:
            min_value = curr_heuristic
            next_steps = [move]
        elif curr_heuristic == min_value:
            next_steps.append(move)
        swap_position(zero_position, move, game_plan)

    print(f'Best heuristic moves: {next_steps}')
    for next_step in next_steps:
        game_plan_cpy = game_plan
        swap_position(zero_position, next_step, game_plan_cpy)
        game_end: bool = game_plan_cpy == end_state
        if (game_end):
            print('game_end')
            print_game_plan(game_plan)
            return
       
        generated_hash = generate_hash(game_plan_cpy)
        if generated_hash in visited_states:
            if visited_states[generated_hash] != game_plan_cpy:
                print('error')
                pp.pprint(visited_states)
                index = 0
                # exit(1)
                while True:
                    index += 1
                    l = int(generated_hash, 16) + index
                    if l not in visited_states:
                        visited_states[l] = game_plan_cpy
                        break
                    print('asd')
            else:      
                print('continue')
                continue

        add_visited_state(visited_states, game_plan_cpy)
        print('After:')
        print_game_plan(game_plan)
        _solve_game([i for i in game_plan_cpy], next_step)


    # print_game_plan(game_plan)
    # # input('')
    # print('\n\n\n')



def get_inversion_count(game_plan: List[int], zero_position_row) -> int:
    """
        Calculates amount of inversions in the game plan
    """
    inversion_count = 0
    for comp_index, comp_value in enumerate(game_plan):
        if comp_value == 0:
            continue
        for index in range(comp_index, len(game_plan)):
            if game_plan[index] != 0 and comp_value > game_plan[index]:
                inversion_count += 1

    return inversion_count


def is_solvable(game_plan: List[int], zero_position_row) -> bool:
    inversion_count_end_state = 0 # get_zero_position_row(end_state)
    zero_position_row = get_zero_position_row(game_plan)
    actual_inversion_count = get_inversion_count(game_plan, zero_position_row)
    # print(zero_position_row)
    # print(inversion_count_end_state, actual_inversion_count, actual_inversion_count + zero_position_row)
    return (inversion_count_end_state % 2) == (actual_inversion_count % 2) and (zero_position_row == (2 % 2))


def get_zero_position_row(game_plan: List[int]):
    for index, number in enumerate(game_plan, start=0):
        if number == 0:
            return index // 3
        

def get_zero_position(game_plan: List[int]):
    for index, number in enumerate(game_plan, start=0):
        if number == 0:
            return (index // 3, (index) % 3)


def generate_hash(game_plan: List[int]):
    combo_str = str(game_plan).encode()
    hash_obj = hashlib.sha512(combo_str)
    return hash_obj.hexdigest()


def add_visited_state(visited_states, game_plan: List[int]):
    hashed_value = generate_hash(game_plan)
    if hashed_value not in visited_states:
        visited_states[hashed_value] = game_plan
        return True
    return False

import yaml


gp = [8, 1, 2, 0, 4, 3, 7, 6, 5]
zero_position = (1, 0)
zero_position_row = 0 #get_zero_position_row(gp)
inversion_count_end_state = get_inversion_count(end_state, zero_position_row)


def test_is_solvable():
    with open('tests/solvable.yaml', 'r') as file:
        parsed_file = yaml.safe_load(file)
        index = 0
        for combination in parsed_file:
            solve_game(combination, get_zero_position(combination))

            index += 1
            if is_solvable(combination, 0):
                print(f'solvable: {combination}')
            else:
                print(f'not solvable: {combination}')
            if (index == 3):
                return
            
def get_moves(game_info, zero_position):
    possible_moves = get_possible_moves(zero_position)
    print(f'possMoves: {possible_moves}')
    print('Before:')  
    print_game_plan(game_info['state'])
    min_value = 10_000
    next_steps = []
    for move in possible_moves:
        swap_position(zero_position, move, game_info)
        curr_heuristic = heuristic_1(game_info['state'])
        if curr_heuristic < min_value:
            min_value = curr_heuristic
            next_steps = [move]
        elif curr_heuristic == min_value:
            next_steps.append(move)
        swap_position(zero_position, move, game_info)
    return next_steps
            

def s(game_plan: List[int], zero_position):
    moves = Queue()
    moves.put({
        'move': zero_position,
        'state': game_plan
    })
    while True:
        next_move = moves.get()
        if next_move is None: 
            break

        zero_pos = get_zero_position(next_move['state'])
        
        swap_position(zero_pos, next_move['move'], next_move)
        # print_game_plan(next_move['state'])
        # input('')

        if next_move['state'] == end_state:
            print('game end')
            print_game_plan(next_move['state'])
            break


        next_moves = get_moves(next_move, get_zero_position(next_move['state']))

        for current_move in next_moves:
            moves.put({
                'move': current_move,
                'state': [value for value in next_move['state']]
            })


if __name__ == '__main__':
    # solve_game(start_state, zero_position)
    # zero_position = (1, 0)
    # zero_position_row = get_zero_position_row([8, 6, 7, 4, 2, 3, 5, 0, 1])
    # inversion_count_end_state = get_inversion_count(end_state, zero_position_row)
    # act= [8, 7, 6, 5, 3, 0, 1, 4, 2]
    # print(get_zero_position_row(act))
    # print(is_solvable(act, 0))

    

    # add_visited_state(visited_states, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
    # # print(is_solvable(gp, zero_position_row))
    # print(visited_states)

    # nodes = Queue()
    # nodes.put(1)
    # nodes.put(2)
    # nodes.put(3)
    # print(nodes.queue)
    # nodes.get()
    # print(nodes.queue)

    # nodes.get()
    # print(nodes.queue)



    act= [0, 1, 2, 3, 4, 5, 6, 7, 8]
    s(act, get_zero_position(act))
    # print(is_solvable(act, get_zero_position_row(act)))
    # solve_game(act, get_zero_position(act))

    # input('')
    # test_is_solvable()
    pass

