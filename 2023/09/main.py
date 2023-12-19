import lib.aoc as aoc

def solve_pattern(p):
    if not any(p): return 0
    return p[-1] + solve_pattern([b-a for a,b in zip(p, p[1:])])

patterns = []
for line in aoc.input_lines():
    patterns.append([int(x) for x in line.split()])

aoc.output(sum(solve_pattern(p) for p in patterns))
aoc.output(sum(solve_pattern(p[::-1]) for p in patterns))
