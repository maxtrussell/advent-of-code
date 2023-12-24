import lib.aoc as aoc
from lib.grid import Grid, Point

def expand(galaxies, scale):
    prev = galaxies[0]
    exp = 0
    for i, g in enumerate(galaxies):
        if g != prev:
            d = g - prev
            exp += (d-1) * scale
            prev = g
        galaxies[i] += exp

grid = Grid(aoc.input_lines())
galaxies = [p for p in grid if grid[p] == '#']
for scale in [1, 999_999]:
    galaxies.sort(key=lambda p: p.x)
    xs = [g.x for g in galaxies]
    expand(xs, scale)

    galaxies.sort(key=lambda p: p.y)
    ys = [g.y for g in galaxies]
    expand(ys, scale)

    ans = 0
    expanded = [Point(x,y) for x,y in zip(xs,ys)]
    for a in expanded:
        for b in expanded:
            if a == b: continue
            ans += abs(a.x - b.x) + abs(a.y - b.y)
    aoc.output(ans // 2)
