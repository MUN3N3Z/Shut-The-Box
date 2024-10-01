from sys import argv
from typing import Tuple, List, Dict
from itertools import combinations
from decimal import Decimal, getcontext
from json import load

ONE_DIE_PROBABILITY = Decimal(1)/Decimal(6)

def parse_input():
    """
    Parse the program's arguments.
    *****Args: Use 'parse args' module to parse the arguments.*****
    """
    current_player = 1 if argv[1] == '--one' else 2
    expected_or_move = argv[2][2:]
    position = tuple(map(int, argv[3]))
    player1_score = int(argv[4]) if current_player == 2 else None
    sum_for_roll = None
    if expected_or_move == 'move':
        sum_for_roll = int(argv[4] if current_player == 1 else argv[5])

    return current_player, expected_or_move, position, player1_score, sum_for_roll

def expectimax(state: Tuple[Tuple[int], int | None, int | None], win_probability: Dict[Tuple, Decimal]) -> Decimal:
    """
    Use memoization to compute the expected value of the game state.
    Args:
        state: (tiles, roll, target)
    """
    tiles, roll, target = state
    if target is None:
        # Player 1
        if not tiles:
            # Player 1 shut the box
            return Decimal(1)
        else: 
            if state not in win_probability:
                if roll is None:
                    if sum(tiles) > 6:
                        # Roll 2 dice
                        win_probability[state] = sum([Decimal(two_die_probability[str(r)]) * expectimax((tiles, r, target), win_probability) for r in range(2, 13)])
                    else:
                        # Roll 1 die
                        win_probability[state] = sum([ONE_DIE_PROBABILITY * expectimax((tiles, r, target), win_probability) for r in range(1, 7)])
                else:
                    moves = possible_moves[f'{sorted(tiles)}, {roll}']
                    if not moves:
                        # No possible moves for player 1, switch to player 2
                        win_probability[state] = Decimal(1) - expectimax((tuple(range(1, 10)), None, sum(tiles)), win_probability)
                    else:
                        # maximize expected value of game over all possible moves
                        win_probability[state] = max([expectimax((tuple(set(tiles) - set(move)), None, target), win_probability) for move in moves])
    else:
        if sum(tiles) < target:
            # Player 2 achieved a lower score than player 1
            return Decimal(1)
        if state not in win_probability:
            if roll is None:
                if sum(tiles) > 6:
                    # Roll 2 dice
                    win_probability[state] = sum([Decimal(two_die_probability[str(r)]) * expectimax((tiles, r, target), win_probability) for r in range(2, 13)])
                else:
                    # Roll 1 die
                    win_probability[state] = sum([ONE_DIE_PROBABILITY * expectimax((tiles, r, target), win_probability) for r in range(1, 7)])
            else:
                moves = possible_moves[f'{sorted(tiles)}, {roll}']
                if not moves:
                    # Player 2 cannot play
                    if sum(tiles) == target:
                        return Decimal(0.5)
                    elif sum(tiles) > target:
                        # Player 2 achieved a lower score than player 1
                        return Decimal(0)
                else:
                    # maximize expected value of game over all possible moves
                    win_probability[state] = max([expectimax((tuple(set(tiles) - set(move)), None, target), win_probability) 
                                                  for move in moves])

    return win_probability[state]

def load_precomputed_data(filename: str) -> dict:
    """
    Load precomputed data from a JSON file.
    """
    with open(filename, 'r') as f:
        return load(f)
    
if __name__ == "__main__":
    current_player, expected_or_move, position, player1_score, sum_for_roll = parse_input()
    with open('precomputations.json', 'r') as f:
        precomputed_data = load(f)
        two_die_probability = precomputed_data['two_die_probability']
        possible_moves = precomputed_data['possible_moves']
        win_probability = dict()
        getcontext().prec = 10
        if expected_or_move == 'expect':
            if current_player == 1:
                result = expectimax((position, None, None), win_probability)
            else:
                result = expectimax((position, None, player1_score), win_probability)
            print(f"{result:.6f}")
        elif expected_or_move == 'move':
            moves = possible_moves[f'{sorted(position)}, {sum_for_roll}']
            if current_player == 1:
                best_move = max(moves, key=lambda x: expectimax((tuple(set(position) - set(x)), None, None), win_probability))
            else:
                best_move = max(moves, key=lambda x: expectimax((tuple(set(position) - set(x)), None, player1_score), win_probability))
            print(f"[{','.join(map(str, sorted(best_move)))}]")