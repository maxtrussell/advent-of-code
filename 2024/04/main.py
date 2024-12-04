import lib.aoc as aoc
from lib.grid import Grid, Point


def word_from_mask(p: Point, g: Grid, mask: list[Point]):
    return "".join(g[p + d] for d in mask if g.in_bounds(p + d))


p1_masks = [
    # Right
    [Point(x, 0) for x in range(4)],
    # Down
    [Point(0, y) for y in range(4)],
    # Down and right
    [Point(d, d) for d in range(4)],
    # Down and left
    [Point(-d, d) for d in range(4)],
]
p1_targets = {"XMAS", "SAMX"}

p2_masks = [
    # Down and left
    [Point(-1, -1), Point(0, 0), Point(1, 1)],
    # Up and right
    [Point(-1, 1), Point(0, 0), Point(1, -1)],
]
p2_targets = {"MAS", "SAM"}

p1, p2 = 0, 0
grid = Grid(aoc.input_lines())
for p in grid:
    if grid[p] in {"X", "S"}:
        p1 += sum(word_from_mask(p, grid, m) in p1_targets for m in p1_masks)
    elif grid[p] == "A":
        p2 += all(word_from_mask(p, grid, m) in p2_targets for m in p2_masks)

aoc.output(p1)
aoc.output(p2)
