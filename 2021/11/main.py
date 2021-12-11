from itertools import product
import fileinput

def get_neighbors(x, y, grid):
    # This time with diagonals
    rows, cols = len(grid), len(grid[0])
    bounds_check = lambda n: 0 <= n[0] < cols and 0 <= n[1] < rows
    deltas = filter(lambda delta: delta != (0, 0), product([-1, 0, 1], repeat=2))
    return filter(bounds_check, map(lambda d: (x+d[0], y+d[1]), deltas))

def flash(x, y, grid, flashes):
    if grid[y][x] > 9 and (x, y) not in flashes:
        flashes.add((x, y))
        for nx, ny in get_neighbors(x, y, grid):
            grid[ny][nx] += 1
        return True
    return False

grid = [[int(x) for x in row.strip()] for row in fileinput.input()]
num_octopodes = sum(map(len, grid))
num_flashes = 0
i = 0
while True:
    i += 1

    # Step 1: increment octopodes
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] += 1

    # Step 2: flash
    flashed = True
    flashes = set()
    while flashed:
        flashed = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                flashed = flashed or flash(x, y, grid, flashes)
    num_flashes += len(flashes)

    if i == 100:
        print('Part 1:', num_flashes)

    if len(flashes) == num_octopodes:
        print('Part 2:', i)
        break

    # Step 3: reset flashed octopodes to zero
    for x, y in flashes:
        grid[y][x] = 0
