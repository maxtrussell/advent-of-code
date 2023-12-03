from lib import aoc
from lib.grid import Grid, Point

from math import prod

def get_number_points(grid: Grid, p: Point) -> list[Point]:
    # Move point to beginning of number
    while grid.in_bounds(p - Point(1, 0)) and grid[p - Point(1, 0)].isdigit():
        p -= Point(1, 0)

    points: list[Point] = []
    while grid.in_bounds(p) and grid[p].isdigit():
        points.append(p)
        p += Point(1, 0)

    return points

def points_to_int(grid: Grid, points: list[Point]) -> int:
    return int(''.join([grid[p] for p in points]))

seen = set()
grid = Grid(aoc.input_lines(), diagonal=True)

is_symbol = lambda p: grid[p] != '.' and not grid[p].isdigit()
is_unseen_number = lambda p: p not in seen and grid[p].isdigit()

part1 = part2 = 0
for p in filter(is_symbol, grid):
    gear_seen = set()
    part_numbers = []
    for n in filter(is_unseen_number, grid.get_neighbors(p)):
        number_points = get_number_points(grid, n)
        seen |= set(number_points)
        gear_seen |= set(number_points)
        part_numbers.append(points_to_int(grid, number_points))

    part1 += sum(part_numbers)
    if grid[p] == '*' and len(part_numbers) == 2:
        part2 += prod(part_numbers)

aoc.output(part1)
aoc.output(part2)
