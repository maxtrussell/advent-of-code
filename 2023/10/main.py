import lib.aoc as aoc
from lib.grid import Grid, Point

pipes = {
    '|': [Point(0, 1), Point(0, -1)],
    '-': [Point(1, 0), Point(-1, 0)],
    'F': [Point(1, 0), Point(0, 1)],
    '7': [Point(-1, 0), Point(0, 1)],
    'J': [Point(-1, 0), Point(0, -1)],
    'L': [Point(1, 0), Point(0, -1)],
}

def inside_loop(p: Point, g: Grid, l: set[Point]):
    xs = 0
    n = p + Point(1, 1)
    while g.in_bounds(n):
        xs += n in l and g[n] not in {'7', 'L'}
        n += Point(1, 1)
    # A point inside the loop will always cross an odd number of times.
    return xs % 2 != 0

def get_next(c: Point, p: Point, g: Grid):
    for d in pipes.get(g[c], []):
        n = c+d
        if n != p: return n
    return None

def find_loop(c: Point, p: Point, g: Grid):
    loop = {c}
    while grid[c] != 'S':
        n = get_next(c, p, g)
        if not n: return set()
        c, p = n, c
        loop.add(c)
    return loop


grid = Grid(aoc.input_lines())
start = next(p for p in grid if grid[p] == 'S')
loop = set()
for n in grid.get_neighbors(start):
    loop = find_loop(n, start, grid)
    if loop:
        aoc.output(round(len(loop) / 2))
        break

count = 0
for p in grid:
    if not p in loop and inside_loop(p, grid, loop):
        count += 1
aoc.output(count)
