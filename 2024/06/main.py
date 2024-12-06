import lib.aoc as aoc
from lib.grid import Grid, Point

dirs = [
    Point(0, -1),  # up
    Point(1, 0),  # right
    Point(0, 1),  # down
    Point(-1, 0),  # left
]
original_path = set()


def walk_guard(curr, facing, seen) -> int:
    while True:
        if aoc.part == 1:
            original_path.add(curr)
        if (curr, facing) in seen:
            # Loop detected
            return 1

        seen.add((curr, facing))
        next_pos = curr + dirs[facing]
        if not grid.in_bounds(next_pos):
            return 0
        elif grid[next_pos] == "#":
            facing = (facing + 1) % len(dirs)
        else:
            curr = next_pos


grid = Grid(aoc.input_lines())
start = next(p for p in grid if grid[p] == "^")

# Collect original path
walk_guard(start, 0, set())
aoc.output(len(original_path))

# Possible obstacle locations are only along the original path.
p2 = 0
for p in original_path - {start}:
    grid[p] = "#"
    p2 += walk_guard(start, 0, set())
    grid[p] = "."
aoc.output(p2)
