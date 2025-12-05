import lib.aoc as aoc
from lib.grid import Grid

g = Grid(aoc.input_lines(), diagonal=True)
removed = True
while removed:
    removed = False
    for p in filter(lambda p: g[p] == "@", g):
        if sum(g[n] == "@" for n in g.get_neighbors(p)) < 4:
            g[p] = "2"
            removed = True
            if sum(g[n] != "." for n in g.get_neighbors(p)) < 4:
                g[p] = "1"


print(sum(g[p] == "1" for p in g))
print(sum(g[p] in ["1", "2"] for p in g))
