import lib.aoc as aoc

from math import prod

def parse_line(line):
    return [int(x) for x in line.split(': ')[1].split()]

def solve_race(time, distance):
    return len([x for x in range(time) if x * (time - x) > distance])

times = parse_line(aoc.input_lines()[0])
distances = parse_line(aoc.input_lines()[1])

part1 = prod(solve_race(times[i], distances[i]) for i in range(len(times)))
part2 = solve_race(int(''.join(map(str, times))), int(''.join(map(str, distances))))

aoc.output(part1)
aoc.output(part2)
