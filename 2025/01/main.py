import lib.aoc as aoc

import math


dial = 50
p1, p2 = 0, 0
for line in aoc.input_lines():
    dir = -1 if line[0] == "L" else 1
    mag = int(line[1:])

    # Account for spins that go more than all the way around.
    p2 += math.floor(mag / 100)
    mag %= 100

    # Detect moves that cross zero
    delta = mag * dir
    if dial != 0 and (dial + delta <= 0 or dial + delta > 99):
        p2 += 1

    dial = (dial + delta) % 100

    p1 += dial == 0

aoc.output(p1)
aoc.output(p2)
