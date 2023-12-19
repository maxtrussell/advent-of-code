import lib.aoc as aoc

import math
import re

# Take a position and return the steps to meet pred.
def solve(pos, dirs, graph, pred) -> int:
    steps = 0
    while not pred(pos):
        l_or_r = 0 if dirs[steps % len(dirs)] == 'L' else 1
        pos = graph[pos][l_or_r] 
        steps += 1
    return steps

dirs = aoc.input_lines()[0]
graph: dict[str, tuple[str, str]] = {}
for line in aoc.input_lines()[2:]:
    m = re.match(r'([A-Z\d]+) = \(([A-Z\d]+), ([A-Z\d]+)\)', line)
    assert m
    key, left, right = m.groups()
    graph[key] = (left, right)

# Part 1
steps = solve('AAA', dirs, graph, lambda x: x == 'ZZZ')
aoc.output(steps)

# Part 2
positions = [x for x in graph.keys() if x.endswith('A')]
steps = []
for pos in positions:
    steps.append(solve(pos, dirs, graph, lambda x: x.endswith('Z')))
aoc.output(math.lcm(*steps))
