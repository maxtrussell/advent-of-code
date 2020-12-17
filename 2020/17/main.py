import itertools
import sys

def simulate_rounds(active_cells, part1=False):
    for _ in range(6):
        active_cells = simulate_round(active_cells, part1=part1)
    return active_cells

def simulate_round(active_cells, part1=False):
    """
    Similar to day 11 but with two significant differences:
    - more dimensions
    - expanding bounding box, means I use a set of active cells rather
      than a full grid made of lists
    """
    new_active_cells = set()
    neighbors = [
        (x, y, z, w) for x,y,z,w in itertools.product([-1, 0, 1], repeat=4)
        if not x == y == z == w == 0
        and not (part1 and x == y == z == 0)
    ]

    # The cells that may potentially change are all active cells
    # and all cells neighboring active cells
    potential_changes = set()
    for x,y,z,w in active_cells:
        for dx,dy,dz,dw in neighbors:
            potential_changes.add((x+dx, y+dy, z+dz, (w+dw) if not part1 else 0))
    potential_changes |= active_cells

    for x, y, z, w in potential_changes:
        curr_cell = (x,y,z,w)
        active_neighbors = len(
            [(dx,dy,dz,dw) for dx,dy,dz,dw in neighbors
                if (x+dx, y+dy, z+dz, w+dw) in active_cells]
        )
        if curr_cell in active_cells and active_neighbors in {2, 3}:
            new_active_cells.add((x,y,z,w))
        elif curr_cell not in active_cells and active_neighbors == 3:
            new_active_cells.add((x,y,z,w))
    return new_active_cells

active_cells = set()
with open(sys.argv[1], 'rt') as f:
    for y, line in enumerate(f.readlines()):
        for x, cell in enumerate(line):
            if cell == '#':
                active_cells.add((x,y,0,0))

# Part 1
part1_active_cells = simulate_rounds(active_cells, part1=True)
print(f'Part 1: {len(part1_active_cells)}')

# Part 2
part2_active_cells = simulate_rounds(active_cells)
print(f'Part 1: {len(part2_active_cells)}')
