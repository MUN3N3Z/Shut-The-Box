from collections import defaultdict
from decimal import Decimal
from typing import Tuple, List, Dict
from itertools import combinations
from json import dump

POSSIBLE_TILES = [comb for i in range(1, 10) for comb in combinations(range(1, 10), i)]

def compute_probabilities(n: int) -> dict:
    """
    Compute the probability of rolling every possible face sum, given n dice.
        n - number of dice
    """
    sum_counts = defaultdict(int)
    def roll_dice(dice: int, total: int):
        if dice == 0:
            sum_counts[total] += 1
            return
        for i in range(1, 7):
            roll_dice(dice - 1, total + i)
    roll_dice(n, 0)

    return {k: v/6**n for k, v in sum_counts.items()}

def compute_possible_moves() -> Dict[int, List[Tuple[int]]]:
    """
    Return all possible combinations of length 1 to len(tiles) that sum to all possible rolls.
    """
    possible_moves = defaultdict(list)
    for tiles in POSSIBLE_TILES:
        for roll in range(1, 13):
            possible_moves[f'{sorted(tiles)}, {roll}'] = [comb for i in range(1, len(tiles) + 1) for comb in combinations(tiles, i) if sum(comb) == roll]
    return possible_moves

def save_precomputed_data(filename: str, data: dict):
    """
    Save precomputed data to a JSON file.
    """
    with open(filename, 'w') as f:
        dump(data, f)

if __name__ == '__main__':
    precomputations = {}
    precomputations['two_die_probability'] = compute_probabilities(2)
    precomputations['possible_moves'] = compute_possible_moves()
    save_precomputed_data('precomputations.json', precomputations)
