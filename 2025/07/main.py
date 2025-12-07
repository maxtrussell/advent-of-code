import lib.aoc as aoc
from lib.grid import Grid, Point

from functools import cache

# Make grid and splits global for easier caching of dfs.
grid = Grid(aoc.input_lines())
splits = set()


@cache
def dfs(p: Point) -> int:
    global grid, splits
    if not grid.in_bounds(p):
        return 1

    if grid[p] == "^":
        splits.add(p)
        return dfs(p + Point(-1, 0)) + dfs(p + Point(1, 0))
    else:
        return dfs(p + Point(0, 1))


num_paths = dfs(next(p for p in grid if grid[p] == "S"))
aoc.output(len(splits))
aoc.output(num_paths)
