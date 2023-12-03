import lib.aoc as aoc

from functools import reduce
from operator import mul
import re

constraint = {'red': 12, 'green': 13, 'blue': 14}

# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
def parse_game(line: str) -> dict[str, int]:
    # Distinguishing between semicolons and commas does not matter.
    draws = [x.split(' ') for x in re.split(', |; ', line.split(': ')[1])]
    game = {k:0 for k in constraint.keys()}
    for num, color in draws:
        game[color] = max(game[color], int(num))
    return game

games = [parse_game(l) for l in aoc.input_lines()]
part1 = part2 = 0
for i, game in enumerate(games, start=1):
    part1 += all(game[color] <= num for color, num in constraint.items()) * i
    part2 += reduce(mul, game.values())
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
